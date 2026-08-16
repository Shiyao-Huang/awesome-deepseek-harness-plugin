import assert from 'node:assert/strict'
import test from 'node:test'

import {installedPlugins, pluginCommandArgs, safeProfileName} from '../lib/runtime.js'


test('plugin manager builds fixed argv without a shell command string', () => {
  assert.deepEqual(pluginCommandArgs({profile: 'web', action: 'add', target: '@owner/example'}), [
    'plugin', '--profile', 'web', 'add', '@owner/example',
  ])
  assert.deepEqual(pluginCommandArgs({profile: 'bad;profile', action: 'list'}), [
    'plugin', '--profile', 'web', 'list', '--depth', '0', '--json',
  ])
  assert.equal(safeProfileName('dev_2'), 'dev_2')
  assert.throws(() => pluginCommandArgs({profile: 'web', action: 'exec', target: 'whoami'}), /unsupported/)
})


test('installed plugin output is normalized and sorted', () => {
  assert.deepEqual(installedPlugins(JSON.stringify([{
    dependencies: {
      zebra: {version: '2.0.0', path: '/plugins/zebra'},
      alpha: {version: '1.0.0'},
    },
  }])), [
    {name: 'alpha', version: '1.0.0', path: null},
    {name: 'zebra', version: '2.0.0', path: '/plugins/zebra'},
  ])
  assert.throws(() => installedPlugins('null'), /invalid plugin list/)
})
