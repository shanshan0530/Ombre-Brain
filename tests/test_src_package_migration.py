"""Regression checks for the gradual migration of flat ``src`` modules."""


def test_memory_messages_legacy_import_is_the_canonical_function():
    from memory_messages import resolved_hint as legacy_resolved_hint
    from ombrebrain.domain.memory_messages import resolved_hint

    assert legacy_resolved_hint is resolved_hint
    assert resolved_hint(True) == "已沉底，只在关键词触发时重新浮现"
    assert resolved_hint(False) == "已重新激活，将参与浮现排序"
