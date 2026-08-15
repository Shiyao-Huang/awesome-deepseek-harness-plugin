const NPM_SPEC = /^(?:@[a-z0-9-~][a-z0-9-._~]*\/)?[a-z0-9-~][a-z0-9-._~]*$/
const GITHUB_SPEC = /^github:[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+(?:#path:\/[A-Za-z0-9._~/-]+)?$/


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
    ...(plugin.tags ?? []),
  ].filter(Boolean).join(' ').toLocaleLowerCase()
}


function relevanceScore(plugin, query) {
  if (!query) return 0
  const name = String(plugin.name ?? '').toLocaleLowerCase()
  const id = String(plugin.id ?? '').toLocaleLowerCase()
  let score = 0
  if (name === query || id === query) score += 100
  if (name.startsWith(query) || id.startsWith(query)) score += 40
  if (name.includes(query) || id.includes(query)) score += 20
  score += (plugin.tags ?? []).filter((tag) => String(tag).toLocaleLowerCase().includes(query)).length * 8
  return score
}


/** Search current plugins and rank textual relevance before native GitHub stars. */
export function searchPlugins(registry, {query = '', category, verifiedOnly = false, limit = 10} = {}) {
  const normalizedQuery = String(query ?? '').trim().toLocaleLowerCase()
  const terms = normalizedQuery.split(/\s+/u).filter(Boolean)
  const boundedLimit = Math.max(1, Math.min(Number.isSafeInteger(limit) ? limit : 10, 100))
  const matches = registry.plugins.filter((plugin) => {
    if (category && plugin.category !== category) return false
    if (verifiedOnly && plugin.verified !== true) return false
    const haystack = searchableText(plugin)
    return terms.every((term) => haystack.includes(term))
  })
  matches.sort((left, right) => {
    const relevance = relevanceScore(right, normalizedQuery) - relevanceScore(left, normalizedQuery)
    if (relevance !== 0) return relevance
    const stars = (right.stars ?? -1) - (left.stars ?? -1)
    if (stars !== 0) return stars
    return String(left.name).localeCompare(String(right.name))
  })
  return {total: matches.length, plugins: matches.slice(0, boundedLimit)}
}


/** Resolve one exact plugin identity by stable id or normalized install spec. */
export function pluginDetails(registry, {id, spec} = {}) {
  const plugin = registry.plugins.find((candidate) => (
    (id && candidate.id === id) || (spec && candidate.install?.spec === spec)
  )) ?? null
  return {plugin}
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
  const missing = []
  for (const id of [...new Set(requested)]) {
    const plugin = registry.plugins.find((candidate) => candidate.id === id)
    if (!plugin || !isSafeInstallSpec(plugin.install?.spec)) {
      missing.push(id)
      continue
    }
    commands.push(`dsh plugin --profile ${safeProfile} add ${plugin.install.spec}`)
  }
  return {
    profile: safeProfile,
    count: commands.length,
    commands,
    missing,
    requiresConfirmation: true,
    note: 'Review source attribution and commands with the user. Run only after the user explicitly confirms installation.',
  }
}
