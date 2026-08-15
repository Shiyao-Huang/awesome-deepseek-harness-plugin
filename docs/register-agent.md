# Agent registration protocol

Use this protocol when a user asks an Agent to register a DeepSeek Harness plugin with `deeplugin.store`. The source-local fields, example, and validation rules live in the [human registration guide](register.md); the public [JSON Schema](https://deeplugin.store/data/market-registry.schema.json) describes the generated output after source attribution and stable-id derivation. Do not invent another input format.

## Required workflow

1. Read the plugin repository, package metadata, release/version evidence, and exact DSH installation documentation.
2. Search the current [public registry](https://deeplugin.store/data/market-registry.json) by normalized install spec. A matching spec is the same Market Plugin even when its name or homepage differs.
3. Choose the narrowest registration route: add one entry to `registry/plugins.json`, or connect an existing public registry in `config/sources.json` when it owns multiple Listings.
4. Copy only public, attributable facts. Missing stars, versions, and metrics are `null`; never estimate them.
5. Use only an npm package name or `github:owner/repository#path:/subdirectory` as the install spec. Never insert a shell command, URL, branch selector, local path, environment assignment, or option flag.
6. Set `verified` to `false`. Do not convert release, popularity, ownership, or a successful local install into a verification claim.
7. Update the source registry's `count` and UTC `updated` date, run the checks in the human guide, and inspect the generated diff for unrelated changes.
8. Show the proposed Listing, source attribution, and validation output to the user. Creating a pull request or sending data to an external service requires the user's authorization.

## Installation safety

Registration does not authorize installation. The `deeplugin_install_plan` tool may return a source-declared command only for a known safe registry spec and always sets `requiresConfirmation: true`. Show the repository, all Registry Source attributions, version claim, and exact command before asking for confirmation. Never execute the plan automatically.

## Expected result

Report the source-local Listing id, normalized install spec, deterministic public id, files changed, validation commands, and expected next observation window. After merge, the two-hour collector preserves the source response as raw evidence, writes a versioned SQLite observation, and regenerates all three byte-identical registry mirrors.
