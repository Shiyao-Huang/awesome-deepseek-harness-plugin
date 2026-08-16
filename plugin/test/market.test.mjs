import assert from 'node:assert/strict'
import test from 'node:test'

import {
  installPlan,
  isSafePackageName,
  packDetails,
  pluginDetails,
  registryStats,
  resolveInstallTarget,
  searchPlugins,
  validateRegistry,
} from '../lib/market.js'


const REGISTRY = {
  version: 3,
  updated: '2026-08-16',
  count: 3,
  verifiedCount: 1,
  packCount: 1,
  plugins: [
    {
      id: 'deeplugin-a',
      name: 'Search Files',
      author: 'alpha',
      category: 'tools',
      description: 'Search workspace files',
      description_zh: '搜索工作区文件',
      install: {target: 'npm', spec: '@alpha/search-files'},
      version: '1.0.0',
      homepage: 'https://github.com/alpha/search-files',
      verified: true,
      stars: 10,
      tags: ['files', 'search'],
      sources: [{registry: 'alpha/registry'}],
    },
    {
      id: 'deeplugin-b',
      name: 'Search Web',
      author: 'beta',
      category: 'tools',
      description: 'Search the public web',
      description_zh: '搜索公开网页',
      install: {target: 'git', spec: 'github:beta/search-web'},
      version: null,
      homepage: 'https://github.com/beta/search-web',
      verified: false,
      stars: 30,
      tags: ['search', 'web'],
      sources: [{registry: 'beta/registry'}],
    },
    {
      id: 'deeplugin-c',
      name: 'Memory',
      author: 'gamma',
      category: 'memory',
      description: 'Persistent memory',
      description_zh: '持久记忆',
      install: {target: 'npm', spec: 'dsh-memory'},
      version: null,
      homepage: 'https://github.com/gamma/memory',
      verified: false,
      stars: null,
      tags: ['memory'],
      sources: [{registry: 'gamma/registry'}],
    },
  ],
  packs: [{
    id: 'deeplugin-pack-aaaaaaaaaaaaaaaaaaaa',
    slug: 'connected-search',
    version: '1.0.0',
    name: 'Connected search',
    name_zh: '联网搜索',
    description: 'Search files and the public web.',
    description_zh: '搜索文件和公开网页。',
    task: 'Search local and public sources.',
    task_zh: '搜索本地与公开来源。',
    maintainer: 'deeplugin.store',
    observedAt: '2026-08-16T08:00:00Z',
    datasetVersion: 'pack-v20260816T080000Z',
    source: {path: 'registry/packs.json', sha256: 'a'.repeat(64)},
    memberCount: 2,
    installable: true,
    missingMembers: [],
    missingVersions: ['deeplugin-b'],
    members: [{
      order: 1,
      pluginId: 'deeplugin-a',
      name: 'Search Files',
      install: {target: 'npm', spec: '@alpha/search-files'},
      relationship: 'complement',
      group: 'search-stack',
      reason: 'Search local files.',
      reason_zh: '搜索本地文件。',
      available: true,
      version: '1.0.0',
      homepage: 'https://github.com/alpha/search-files',
      provenance: [{registry: 'alpha/registry', rawSnapshotId: 1, spec: '@alpha/search-files'}],
    }, {
      order: 2,
      pluginId: 'deeplugin-b',
      name: 'Search Web',
      install: {target: 'git', spec: 'github:beta/search-web'},
      relationship: 'complement',
      group: 'search-stack',
      reason: 'Search public sources.',
      reason_zh: '搜索公开来源。',
      available: true,
      version: null,
      homepage: 'https://github.com/beta/search-web',
      provenance: [{registry: 'beta/registry', rawSnapshotId: 2, spec: 'github:beta/search-web'}],
    }],
  }],
}


test('search ranks matching plugins and supports category and source-verified filters', () => {
  assert.deepEqual(
    searchPlugins(REGISTRY, {query: 'search'}).plugins.map((plugin) => plugin.id),
    ['deeplugin-b', 'deeplugin-a'],
  )
  assert.equal(searchPlugins(REGISTRY, {query: '搜索工作区'}).plugins[0].id, 'deeplugin-a')
  assert.equal(searchPlugins(REGISTRY, {query: 'find a plugin for public web search'}).plugins[0].id, 'deeplugin-b')
  assert.equal(searchPlugins(REGISTRY, {query: '帮我找一个搜索公开网页的插件'}).plugins[0].id, 'deeplugin-b')
  assert.equal(searchPlugins(REGISTRY, {query: 'beta/registry'}).plugins[0].id, 'deeplugin-b')
  assert.equal(searchPlugins(REGISTRY, {category: 'memory'}).total, 1)
  assert.equal(searchPlugins(REGISTRY, {verifiedOnly: true}).plugins[0].id, 'deeplugin-a')
  assert.equal(searchPlugins(REGISTRY, {limit: 1}).plugins.length, 1)
})


test('details resolve an exact registry id or install spec with source attribution', () => {
  assert.equal(pluginDetails(REGISTRY, {id: 'deeplugin-b'}).plugin.install.spec, 'github:beta/search-web')
  assert.equal(pluginDetails(REGISTRY, {spec: '@alpha/search-files'}).plugin.id, 'deeplugin-a')
  assert.equal(pluginDetails(REGISTRY, {id: 'missing'}).plugin, null)
})


test('pack details preserve alternatives, complements, missing versions, and provenance', () => {
  const pack = packDetails(REGISTRY, {id: 'deeplugin-pack-aaaaaaaaaaaaaaaaaaaa'}).pack

  assert.equal(pack.version, '1.0.0')
  assert.deepEqual(pack.missingVersions, ['deeplugin-b'])
  assert.deepEqual(pack.members.map((member) => [member.pluginId, member.relationship, member.group]), [
    ['deeplugin-a', 'complement', 'search-stack'],
    ['deeplugin-b', 'complement', 'search-stack'],
  ])
  assert.equal(pack.members[0].provenance[0].rawSnapshotId, 1)
  assert.equal(packDetails(REGISTRY, {id: 'missing'}).pack, null)
})


test('install plan only emits known registry specs and requires explicit confirmation', () => {
  assert.deepEqual(installPlan(REGISTRY, {ids: 'deeplugin-a,missing', profile: 'dev'}), {
    profile: 'dev',
    count: 1,
    commands: ['dsh plugin --profile dev add @alpha/search-files'],
    plugins: [{
      id: 'deeplugin-a',
      name: 'Search Files',
      spec: '@alpha/search-files',
      homepage: 'https://github.com/alpha/search-files',
      verified: true,
      sources: [{registry: 'alpha/registry'}],
    }],
    missing: ['missing'],
    requiresConfirmation: true,
    note: 'Review source attribution and commands with the user. After confirmation, call deeplugin_install with each selected registry id and its exact spec.',
  })
  assert.equal(installPlan(REGISTRY, {ids: 'deeplugin-b', profile: 'bad; profile'}).profile, 'web')
})


test('pack install plan shows every member but still requires one approval per selected plugin', () => {
  const plan = installPlan(REGISTRY, {packId: 'deeplugin-pack-aaaaaaaaaaaaaaaaaaaa', profile: 'research'})

  assert.equal(plan.pack.id, 'deeplugin-pack-aaaaaaaaaaaaaaaaaaaa')
  assert.deepEqual(plan.commands, [
    'dsh plugin --profile research add @alpha/search-files',
    'dsh plugin --profile research add github:beta/search-web',
  ])
  assert.deepEqual(plan.plugins.map((plugin) => ({
    id: plugin.id,
    relationship: plugin.relationship,
    group: plugin.group,
    version: plugin.version,
  })), [{
    id: 'deeplugin-a',
    relationship: 'complement',
    group: 'search-stack',
    version: '1.0.0',
  }, {
    id: 'deeplugin-b',
    relationship: 'complement',
    group: 'search-stack',
    version: null,
  }])
  assert.equal(plan.requiresConfirmation, true)
  assert.match(plan.note, /one deeplugin_install call per selected member/)
})


test('install execution resolves only known registry ids and package management names', () => {
  assert.equal(resolveInstallTarget(REGISTRY, {id: 'deeplugin-b'}).spec, 'github:beta/search-web')
  assert.throws(() => resolveInstallTarget(REGISTRY, {id: 'missing'}), /unknown or unsafe/)
  assert.equal(isSafePackageName('@alpha/search-files'), true)
  assert.equal(isSafePackageName('github:alpha/search-files'), false)
  assert.equal(isSafePackageName('alpha; rm -rf /'), false)
})


test('stats preserve missing metrics and explain verified as source claims', () => {
  assert.deepEqual(registryStats(REGISTRY), {
    total: 3,
    verifiedClaims: 1,
    updated: '2026-08-16',
    byCategory: {memory: 1, tools: 2},
  })
})


test('registry validation rejects count drift and unsafe install specs', () => {
  assert.equal(validateRegistry(REGISTRY), true)
  assert.equal(validateRegistry({...REGISTRY, version: 2}), false)
  assert.equal(validateRegistry({...REGISTRY, count: 2}), false)
  assert.equal(validateRegistry({
    ...REGISTRY,
    plugins: [{...REGISTRY.plugins[0], install: {target: 'git', spec: 'github:alpha/a;touch /tmp/x'}}],
    count: 1,
    verifiedCount: 1,
  }), false)
})
