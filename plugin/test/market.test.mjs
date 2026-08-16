import assert from 'node:assert/strict'
import test from 'node:test'

import {
  installPlan,
  isSafePackageName,
  pluginDetails,
  registryStats,
  resolveInstallTarget,
  searchPlugins,
  validateRegistry,
} from '../lib/market.js'


const REGISTRY = {
  version: 2,
  updated: '2026-08-16',
  count: 3,
  verifiedCount: 1,
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
  assert.equal(validateRegistry({...REGISTRY, count: 2}), false)
  assert.equal(validateRegistry({
    ...REGISTRY,
    plugins: [{...REGISTRY.plugins[0], install: {target: 'git', spec: 'github:alpha/a;touch /tmp/x'}}],
    count: 1,
    verifiedCount: 1,
  }), false)
})
