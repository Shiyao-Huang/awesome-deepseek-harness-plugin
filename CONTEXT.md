# DeepSeek Harness Ecosystem Registry

This context names the public evidence and market concepts used by the aggregator. It separates source claims from the installable plugin identities projected by this repository.

## Language

**Registry Source**:
A public catalog maintained outside this repository whose listings are collected as attributed evidence.
_Avoid_: Official registry, trusted registry

**Registry Snapshot**:
A dated raw capture of one Registry Source, including its declared format version, counts, and collection status.
_Avoid_: Current registry, registry cache

**Listing**:
One Registry Source's claim about a plugin, including its description, install declaration, verification claim, and provenance.
_Avoid_: Plugin record, canonical plugin

**Listing Key**:
A source-local stable identity derived from declared registry id, then exact Install Spec, then canonical public URL and category. It distinguishes multiple installable plugins that share one monorepo homepage.
_Avoid_: Global plugin id, repository id

**Plugin Identity**:
An installable artifact aggregated across Listings, keyed first by normalized Install Spec and otherwise by canonical public URL.
_Avoid_: Listing, repository

**Install Spec**:
The exact package-manager locator declared by a Registry Source, such as an npm package or `github:owner/repo#path:/subdir`.
_Avoid_: Install URL, repository URL

**Active Listing**:
A Listing present in the latest successful snapshot of its source path. A failed or blocked collection does not make a Listing inactive.
_Avoid_: Available plugin, supported plugin

**Verified Listing**:
A source-attributed claim that the curator exercised its stated checks. It is not this repository's security or compatibility endorsement.
_Avoid_: Safe plugin, approved plugin

**Plugin Pack**:
A versioned, task-oriented review aid that names exact Plugin Identities and preserves each member's required, alternative, or complementary relationship. It never means bulk installation.
_Avoid_: Bundle installer, recommended stack, trusted collection

**Pack Version**:
An immutable bilingual Pack definition with its own dataset version, observation date, source path, SHA-256, and ordered member declarations. Any content or status change requires a new Pack Version.
_Avoid_: Latest JSON, mutable preset

**Available Pack Member**:
A declared Pack member whose stable plugin id resolves to the same exact Install Spec in the current Market Registry. Availability does not imply a reported version, compatibility, safety, or quality.
_Avoid_: Verified member, supported member
