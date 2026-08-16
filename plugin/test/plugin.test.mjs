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


test('tool handlers expose discovery, confirmed installation, and profile management', async () => {
  const requests = []
  const runner = async (request) => {
    requests.push(request)
    if (request.action === 'list') {
      return {exitCode: 0, stdout: '[{"dependencies":{"@owner/example":{"version":"1.0.0","path":"/plugins/example"}}}]', stderr: ''}
    }
    return {exitCode: 0, stdout: 'done', stderr: ''}
  }
  const tools = createTools(async () => REGISTRY, runner)
  assert.deepEqual(
    tools.map((tool) => tool.name),
    ['deeplugin_search', 'deeplugin_details', 'deeplugin_stats', 'deeplugin_install_plan', 'deeplugin_install', 'deeplugin_manage'],
  )
  assert.equal((await tools[0].execute({query: 'example'}, {})).plugins[0].id, 'deeplugin-a')
  assert.equal((await tools[1].execute({id: 'deeplugin-a'}, {})).plugin.author, 'owner')
  assert.equal((await tools[2].execute({}, {})).total, 1)
  assert.equal((await tools[3].execute({ids: 'deeplugin-a'}, {})).requiresConfirmation, true)
  assert.equal((await tools[4].execute({id: 'deeplugin-a', spec: '@owner/example', profile: 'web'}, {})).spec, '@owner/example')
  await assert.rejects(
    tools[4].execute({id: 'deeplugin-a', spec: '@owner/other', profile: 'web'}, {}),
    /does not match registry id/,
  )
  assert.deepEqual((await tools[5].execute({action: 'list', profile: 'web'}, {})).installed, [{
    name: '@owner/example',
    version: '1.0.0',
    path: '/plugins/example',
  }])
  assert.deepEqual(requests, [
    {profile: 'web', action: 'add', target: '@owner/example'},
    {profile: 'web', action: 'list'},
  ])
})


test('apply registers tools and approval-gates every mutating operation', async () => {
  const registered = []
  const labels = []
  const listeners = new Map()
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
    on(name, listener) {
      listeners.set(name, listener)
    },
  }

  apply(ctx)

  assert.deepEqual(registered, ['deeplugin_search', 'deeplugin_details', 'deeplugin_stats', 'deeplugin_install_plan', 'deeplugin_install', 'deeplugin_manage'])
  assert.equal(labels.length, 6)
  assert.ok(labels.every((label) => label.startsWith('deeplugin-market: ')))
  const gate = listeners.get('tools/pre-execute')
  assert.deepEqual(await gate({name: 'deeplugin_install', arguments: {id: 'deeplugin-a', spec: '@owner/example', profile: 'web'}}, () => ({kind: 'allow'})), {
    kind: 'ask',
    reason: 'Install registry plugin deeplugin-a with exact spec @owner/example into DSH profile web.',
  })
  assert.deepEqual(await gate({name: 'deeplugin_manage', arguments: {action: 'remove', package: '@owner/example'}}, () => ({kind: 'allow'})), {
    kind: 'ask',
    reason: 'remove installed package @owner/example in DSH profile web.',
  })
  assert.deepEqual(await gate({name: 'deeplugin_manage', arguments: {action: 'list'}}, () => ({kind: 'allow'})), {kind: 'allow'})
})
