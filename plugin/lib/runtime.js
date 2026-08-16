/** Controlled access to the local DSH profile plugin manager. */

import {spawn} from 'node:child_process'


const PROFILE_PATTERN = /^[A-Za-z0-9_-]+$/
const OUTPUT_LIMIT = 64 * 1024


/** Normalize an untrusted profile name without creating a shell argument surface. */
export function safeProfileName(profile) {
  return PROFILE_PATTERN.test(String(profile)) ? String(profile) : 'web'
}


/** Build the exact argv passed to the DSH CLI for one supported operation. */
export function pluginCommandArgs({profile = 'web', action, target}) {
  const args = ['plugin', '--profile', safeProfileName(profile)]
  if (action === 'list') return [...args, 'list', '--depth', '0', '--json']
  if (!['add', 'remove', 'update'].includes(action)) throw new Error(`unsupported plugin action: ${action}`)
  if (typeof target !== 'string' || target.length === 0) throw new Error(`${action} requires a plugin target`)
  return [...args, action, target]
}


function appendBounded(current, chunk) {
  const next = current + chunk.toString('utf8')
  return next.length <= OUTPUT_LIMIT ? next : next.slice(-OUTPUT_LIMIT)
}


/** Run one DSH plugin-management command without invoking a shell. */
export function runDshPlugin(request, execution = {}) {
  const command = process.env.DSH_MARKET_DSH_COMMAND?.trim() || 'dsh'
  const args = pluginCommandArgs(request)
  return new Promise((resolve, reject) => {
    const child = spawn(command, args, {
      shell: false,
      stdio: ['ignore', 'pipe', 'pipe'],
      signal: execution.signal,
    })
    let stdout = ''
    let stderr = ''
    child.stdout.on('data', (chunk) => { stdout = appendBounded(stdout, chunk) })
    child.stderr.on('data', (chunk) => { stderr = appendBounded(stderr, chunk) })
    child.once('error', reject)
    child.once('close', (exitCode, signal) => {
      resolve({
        exitCode: exitCode ?? 1,
        signal,
        stdout: stdout.trim(),
        stderr: stderr.trim(),
      })
    })
  })
}


/** Parse `dsh plugin list --json` into stable dependency records. */
export function installedPlugins(stdout) {
  const parsed = JSON.parse(stdout)
  const profile = Array.isArray(parsed) ? parsed[0] : parsed
  if (!profile || typeof profile !== 'object') throw new Error('DSH returned an invalid plugin list')
  return Object.entries(profile.dependencies ?? {}).map(([name, value]) => ({
    name,
    version: value && typeof value === 'object' ? value.version ?? null : null,
    path: value && typeof value === 'object' ? value.path ?? null : null,
  })).sort((left, right) => left.name.localeCompare(right.name))
}
