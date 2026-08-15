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
