/** Agent-facing deeplugin.store market tools for DeepSeek Harness. */

import {readFileSync} from 'node:fs'
import {defineTool} from '@deepseek-ai/dsh-tools'

import {
  installPlan,
  pluginDetails,
  registryStats,
  searchPlugins,
  validateRegistry,
} from './market.js'


export const name = 'deeplugin-market'
export const inject = ['tools']
export const REGISTRY_URL = 'https://deeplugin.store/data/market-registry.json'


/** Load and validate the registry snapshot shipped in the plugin package. */
export function loadEmbeddedRegistry() {
  const raw = readFileSync(new URL('../data/market-registry.json', import.meta.url), 'utf8')
  const registry = JSON.parse(raw)
  if (!validateRegistry(registry)) throw new Error('embedded deeplugin registry is invalid')
  return registry
}


/** Fetch the live registry with a bounded timeout and an offline snapshot fallback. */
export async function loadRegistry(signal) {
  const timeout = new AbortController()
  const timer = setTimeout(() => timeout.abort(), 5000)
  try {
    const combined = AbortSignal.any([signal ?? timeout.signal, timeout.signal])
    const response = await fetch(REGISTRY_URL, {
      signal: combined,
      headers: {'User-Agent': 'deeplugin-market/0.1'},
    })
    if (!response.ok) throw new Error(`registry HTTP ${response.status}`)
    const registry = await response.json()
    if (!validateRegistry(registry)) throw new Error('live deeplugin registry is invalid')
    return registry
  } catch {
    return loadEmbeddedRegistry()
  } finally {
    clearTimeout(timer)
  }
}


/** Create the four market tools around an injectable registry loader. */
export function createTools(registryLoader = loadRegistry) {
  return [
    defineTool({
      name: 'deeplugin_search',
      description: 'Search the attributed DeepSeek Harness plugin registry by intent, name, author, category, tags, and bilingual descriptions. Results are ranked by relevance and GitHub stars.',
      parameters: {
        query: {type: 'string', description: 'Plugin intent or free-text query; empty returns the most starred entries'},
        category: {type: 'string', description: 'Optional exact category filter'},
        verifiedOnly: {type: 'boolean', description: 'Only entries with at least one source curator verification claim'},
        limit: {type: 'integer', description: 'Maximum results, 1-100; default 10'},
      },
      output: {
        schema: {
          type: 'object',
          additionalProperties: false,
          properties: {
            total: {type: 'integer', required: true},
            plugins: {type: 'array', required: true, items: {type: 'object', additionalProperties: true}},
          },
        },
        render: (_args, value) => [{
          type: 'text',
          text: `${value.total} matching plugin(s).\n${value.plugins.map((plugin) => (
            `- ${plugin.name} (${plugin.id}, ${plugin.category}, ${plugin.stars ?? 'stars unavailable'}): ${plugin.description}`
          )).join('\n')}`,
        }],
      },
      async execute(args, execution) {
        const registry = await registryLoader(execution?.signal)
        return searchPlugins(registry, {
          query: args.query ?? '',
          category: args.category,
          verifiedOnly: args.verifiedOnly === true,
          limit: typeof args.limit === 'number' ? args.limit : 10,
        })
      },
      presentCall: (args) => ({card: 'generic', title: `deeplugin search: ${args.query ?? 'top'}`, kind: 'read', rawInput: args}),
    }),
    defineTool({
      name: 'deeplugin_details',
      description: 'Read one deeplugin registry entry by stable id or exact install spec, including every source attribution and verification claim.',
      parameters: {
        id: {type: 'string', description: 'Stable deeplugin registry id'},
        spec: {type: 'string', description: 'Exact registry install spec'},
      },
      output: {
        schema: {
          type: 'object',
          additionalProperties: false,
          properties: {
            plugin: {
              oneOf: [
                {type: 'object', additionalProperties: true},
                {type: 'null'},
              ],
              required: true,
            },
          },
        },
        render: (_args, value) => [{
          type: 'text',
          text: value.plugin
            ? `${value.plugin.name}: ${value.plugin.description}\nInstall spec: ${value.plugin.install.spec}\nSources: ${value.plugin.sources.map((source) => source.registry).join(', ')}`
            : 'No registry plugin matched that id or install spec.',
        }],
      },
      async execute(args, execution) {
        return pluginDetails(await registryLoader(execution?.signal), args)
      },
      presentCall: (args) => ({card: 'generic', title: `deeplugin details: ${args.id ?? args.spec ?? 'unknown'}`, kind: 'read', rawInput: args}),
    }),
    defineTool({
      name: 'deeplugin_stats',
      description: 'Report current deeplugin registry counts, source verification claims, update date, and category distribution.',
      parameters: {},
      output: {
        schema: {
          type: 'object',
          additionalProperties: false,
          properties: {
            total: {type: 'integer', required: true},
            verifiedClaims: {type: 'integer', required: true},
            updated: {type: 'string', required: true},
            byCategory: {type: 'object', required: true, additionalProperties: true},
          },
        },
        render: (_args, value) => [{
          type: 'text',
          text: `${value.total} plugins; ${value.verifiedClaims} carry source verification claims; registry updated ${value.updated}.`,
        }],
      },
      async execute(_args, execution) {
        return registryStats(await registryLoader(execution?.signal))
      },
      presentCall: () => ({card: 'generic', title: 'deeplugin registry stats', kind: 'read', rawInput: {}}),
    }),
    defineTool({
      name: 'deeplugin_install_plan',
      description: 'Build exact dsh plugin add commands for stable registry ids. This tool never executes installation; show the source attribution and commands, then require explicit user confirmation before running them.',
      parameters: {
        ids: {type: 'string', description: 'Comma-separated stable ids returned by deeplugin_search'},
        profile: {type: 'string', description: 'Target DSH profile; default web'},
      },
      output: {
        schema: {
          type: 'object',
          additionalProperties: false,
          properties: {
            profile: {type: 'string', required: true},
            count: {type: 'integer', required: true},
            commands: {type: 'array', required: true, items: {type: 'string'}},
            missing: {type: 'array', required: true, items: {type: 'string'}},
            requiresConfirmation: {type: 'boolean', required: true},
            note: {type: 'string', required: true},
          },
        },
        render: (_args, value) => [{
          type: 'text',
          text: `${value.count} reviewable command(s):\n${value.commands.join('\n')}\n${value.note}`,
        }],
      },
      async execute(args, execution) {
        return installPlan(await registryLoader(execution?.signal), {
          ids: args.ids ?? '',
          profile: args.profile ?? 'web',
        })
      },
      presentCall: (args) => ({card: 'generic', title: `deeplugin install plan: ${args.profile ?? 'web'}`, kind: 'other', rawInput: args}),
    }),
  ]
}


/** Register market tools as Cordis effects so disposal follows plugin lifetime. */
export function apply(ctx) {
  for (const tool of createTools()) {
    ctx.effect(() => ctx.tools.register(tool), `deeplugin-market: ${tool.name}`)
  }
}
