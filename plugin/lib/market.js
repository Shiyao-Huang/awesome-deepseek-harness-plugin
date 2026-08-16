const NPM_SPEC = /^(?:@[a-z0-9-~][a-z0-9-._~]*\/)?[a-z0-9-~][a-z0-9-._~]*$/
const GITHUB_SPEC = /^github:[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+(?:#path:\/[A-Za-z0-9._~/-]+)?$/
const WORD_SEGMENTER = new Intl.Segmenter(undefined, {granularity: 'word'})
const QUERY_STOP_WORDS = new Set([
  'a', 'an', 'and', 'can', 'find', 'for', 'i', 'install', 'me', 'need', 'please',
  'plugin', 'plugins', 'show', 'that', 'the', 'to', 'want', 'with',
  '一个', '一款', '可以', '帮', '帮我', '我', '找', '查找', '的', '能', '请', '需要', '想要', '安装', '插件',
])


/** Return whether a registry install spec is safe to place in a displayed command. */
export function isSafeInstallSpec(spec) {
  return typeof spec === 'string' && (NPM_SPEC.test(spec) || GITHUB_SPEC.test(spec))
}


/** Validate the registry invariants required by all market tools. */
export function validateRegistry(registry) {
  if (!registry || registry.version !== 2 || !Array.isArray(registry.plugins)) return false
  if (registry.count !== registry.plugins.length) return false
  const ids = new Set()
  const specs = new Set()
  let verifiedCount = 0
  for (const plugin of registry.plugins) {
    if (!plugin || typeof plugin.id !== 'string' || ids.has(plugin.id)) return false
    ids.add(plugin.id)
    const spec = plugin.install?.spec
    if (!isSafeInstallSpec(spec) || specs.has(spec)) return false
    specs.add(spec)
    if (plugin.verified === true) {
      if (!plugin.version) return false
      verifiedCount += 1
    }
  }
  return registry.verifiedCount === verifiedCount
}


function searchableText(plugin) {
  return [
    plugin.id,
    plugin.name,
    plugin.author,
    plugin.category,
    plugin.description,
    plugin.description_zh,
    plugin.install?.spec,
    ...(plugin.tags ?? []),
    ...(plugin.sources ?? []).map((source) => source?.registry),
  ].filter(Boolean).join(' ').toLocaleLowerCase()
}


function queryTerms(query) {
  const normalized = String(query ?? '').trim().toLocaleLowerCase()
  return [...WORD_SEGMENTER.segment(normalized)]
    .filter((part) => part.isWordLike)
    .map((part) => part.segment)
    .filter((term) => !QUERY_STOP_WORDS.has(term) && (term.length > 1 || /^[a-z0-9]$/u.test(term)))
}


function relevanceScore(plugin, query, terms) {
  if (!query || terms.length === 0) return 0
  const name = String(plugin.name ?? '').toLocaleLowerCase()
  const id = String(plugin.id ?? '').toLocaleLowerCase()
  const category = String(plugin.category ?? '').toLocaleLowerCase()
  const tags = (plugin.tags ?? []).map((tag) => String(tag).toLocaleLowerCase())
  const haystack = searchableText(plugin)
  let score = 0
  if (name === query || id === query) score += 200
  if (name.startsWith(query) || id.startsWith(query)) score += 100
  if (name.includes(query) || id.includes(query)) score += 70
  if (haystack.includes(query)) score += 50
  let matchedTerms = 0
  for (const term of terms) {
    if (!haystack.includes(term)) continue
    matchedTerms += 1
    if (name === term || id === term) score += 80
    else if (name.startsWith(term) || id.startsWith(term)) score += 55
    else if (name.includes(term) || id.includes(term)) score += 35
    if (tags.some((tag) => tag === term)) score += 34
    else if (tags.some((tag) => tag.includes(term))) score += 20
    if (category === term) score += 24
    score += 8
  }
  score += matchedTerms * 12
  score += Math.round(40 * matchedTerms / terms.length)
  if (matchedTerms === terms.length && terms.length > 1) score += 60
  return score
}


/** Search current plugins and rank textual relevance before native GitHub stars. */
export function searchPlugins(registry, {query = '', category, verifiedOnly = false, limit = 10} = {}) {
  const normalizedQuery = String(query ?? '').trim().toLocaleLowerCase()
  const terms = queryTerms(normalizedQuery)
  const boundedLimit = Math.max(1, Math.min(Number.isSafeInteger(limit) ? limit : 10, 100))
  const matches = registry.plugins.flatMap((plugin) => {
    if (category && plugin.category !== category) return []
    if (verifiedOnly && plugin.verified !== true) return []
    const matchedTerms = terms.filter((term) => searchableText(plugin).includes(term)).length
    const minimumTerms = terms.length <= 1 ? terms.length : Math.min(2, Math.ceil(terms.length / 2))
    if (matchedTerms < minimumTerms) return []
    const score = relevanceScore(plugin, normalizedQuery, terms)
    return [{plugin, score}]
  })
  matches.sort((left, right) => {
    const relevance = right.score - left.score
    if (relevance !== 0) return relevance
    const stars = (right.plugin.stars ?? -1) - (left.plugin.stars ?? -1)
    if (stars !== 0) return stars
    return String(left.plugin.name).localeCompare(String(right.plugin.name))
  })
  return {total: matches.length, plugins: matches.slice(0, boundedLimit).map(({plugin}) => plugin)}
}


/** Resolve one exact plugin identity by stable id or normalized install spec. */
export function pluginDetails(registry, {id, spec} = {}) {
  const plugin = registry.plugins.find((candidate) => (
    (id && candidate.id === id) || (spec && candidate.install?.spec === spec)
  )) ?? null
  return {plugin}
}


/** Resolve one registry id to its safe install identity. */
export function resolveInstallTarget(registry, {id} = {}) {
  const plugin = registry.plugins.find((candidate) => candidate.id === id)
  if (!plugin || !isSafeInstallSpec(plugin.install?.spec)) {
    throw new Error(`unknown or unsafe deeplugin registry id: ${id ?? 'missing'}`)
  }
  return {
    id: plugin.id,
    name: plugin.name,
    spec: plugin.install.spec,
    homepage: plugin.homepage,
    verified: plugin.verified === true,
    sources: plugin.sources,
  }
}


/** Return whether a package name is safe to pass as one remove/update argv value. */
export function isSafePackageName(value) {
  return typeof value === 'string' && NPM_SPEC.test(value)
}


/** Summarize the current registry without replacing missing metrics with zero. */
export function registryStats(registry) {
  const byCategory = {}
  for (const category of [...new Set(registry.plugins.map((plugin) => plugin.category))].sort()) {
    byCategory[category] = registry.plugins.filter((plugin) => plugin.category === category).length
  }
  return {
    total: registry.plugins.length,
    verifiedClaims: registry.plugins.filter((plugin) => plugin.verified === true).length,
    updated: registry.updated,
    byCategory,
  }
}


/** Build reviewable commands for known plugins without executing an installation. */
export function installPlan(registry, {ids = '', profile = 'web'} = {}) {
  const safeProfile = /^[A-Za-z0-9_-]+$/.test(String(profile)) ? String(profile) : 'web'
  const requested = Array.isArray(ids)
    ? ids.map(String)
    : String(ids ?? '').split(',').map((value) => value.trim()).filter(Boolean)
  const commands = []
  const plugins = []
  const missing = []
  for (const id of [...new Set(requested)]) {
    const plugin = registry.plugins.find((candidate) => candidate.id === id)
    if (!plugin || !isSafeInstallSpec(plugin.install?.spec)) {
      missing.push(id)
      continue
    }
    commands.push(`dsh plugin --profile ${safeProfile} add ${plugin.install.spec}`)
    plugins.push({
      id: plugin.id,
      name: plugin.name,
      spec: plugin.install.spec,
      homepage: plugin.homepage,
      verified: plugin.verified === true,
      sources: plugin.sources,
    })
  }
  return {
    profile: safeProfile,
    count: commands.length,
    commands,
    plugins,
    missing,
    requiresConfirmation: true,
    note: 'Review source attribution and commands with the user. After confirmation, call deeplugin_install with each selected registry id and its exact spec.',
  }
}
