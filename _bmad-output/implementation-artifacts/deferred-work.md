## Deferred from: code review of 6-1-load-target-specific-powerpoint-template-metadata.md (2026-05-26)

- Disabled target filtering treats string `"false"` as enabled before Pydantic coercion [`src/thucthengay/config/service.py:126`]. This appears pre-existing in `_enabled_targets_only`; it is not introduced by the Story 6.1 PPTX template change.
