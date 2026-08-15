import assert from 'node:assert/strict'
import test from 'node:test'

import {apply, createTools} from '../lib/index.js'


const REGISTRY = {
  version: 2,
  updated: '2026-08-16',
  count: 1,
  verifiedCount: 0,
  plugins: [{
    id: 'deeplugin-a',
    name: 'Example',
    author: 'owner',
    category: 'tools',
    description: 'Example tool',
    description_zh: '示例工具',
    install: {target: 'npm', spec: '@owner/example'},
    version: null,
    homepage: 'https://github.com/owner/example',
    verified: false,
    stars: 1,
    tags: ['tools'],
    sources: [{registry: 'owner/registry'}],
  }],
}


test('tool handlers expose search, details, stats, and confirmation-gated install plans', async () => {
  const tools = createTools(async () => REGISTRY)
  assert.deepEqual(
    tools.map((tool) => tool.name),
    ['deeplugin_search', 'deeplugin_details', 'deeplugin_stats', 'deeplugin_install_plan'],
  )
  assert.equal((await tools[0].execute({query: 'example'}, {})).plugins[0].id, 'deeplugin-a')
  assert.equal((await tools[1].execute({id: 'deeplugin-a'}, {})).plugin.author, 'owner')
  assert.equal((await tools[2].execute({}, {})).total, 1)
  assert.equal((await tools[3].execute({ids: 'deeplugin-a'}, {})).requiresConfirmation, true)
})


test('apply registers every tool through a disposable Cordis effect', () => {
  const registered = []
  const labels = []
  const ctx = {
    tools: {
      register(tool) {
        registered.push(tool.name)
        return () => registered.splice(registered.indexOf(tool.name), 1)
      },
    },
    effect(callback, label) {
      labels.push(label)
      callback()
    },
  }

  apply(ctx)

  assert.deepEqual(registered, ['deeplugin_search', 'deeplugin_details', 'deeplugin_stats', 'deeplugin_install_plan'])
  assert.equal(labels.length, 4)
  assert.ok(labels.every((label) => label.startsWith('deeplugin-market: ')))
})
