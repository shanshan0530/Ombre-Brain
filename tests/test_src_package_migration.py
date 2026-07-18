"""Regression checks for the gradual migration of flat ``src`` modules."""


def test_memory_messages_legacy_import_is_the_canonical_function():
    from memory_messages import resolved_hint as legacy_resolved_hint
    from ombrebrain.domain.memory_messages import resolved_hint

    assert legacy_resolved_hint is resolved_hint
    assert resolved_hint(True) == "已沉底，只在关键词触发时重新浮现"
    assert resolved_hint(False) == "已重新激活，将参与浮现排序"


def test_plan_history_legacy_import_is_the_canonical_function():
    from plan_history import append_plan_change_log as legacy_append
    from ombrebrain.domain.plan_history import append_plan_change_log

    assert legacy_append is append_plan_change_log

    original = [{"action": "created", "to": "pending"}]
    updated = append_plan_change_log(original, "status", to="done", ignored=None)

    assert updated is not original
    assert original == [{"action": "created", "to": "pending"}]
    assert updated[:-1] == original
    assert updated[-1]["action"] == "status"
    assert updated[-1]["to"] == "done"
    assert "ignored" not in updated[-1]
    assert updated[-1]["ts"]


def test_provider_detect_legacy_imports_are_canonical_functions():
    import provider_detect as legacy
    from ombrebrain.integrations import provider_detect

    public_names = (
        "endpoint_hostname",
        "is_gemini_native_host",
        "is_gemini_openai_compat_endpoint",
        "is_known_cloud_embedding_endpoint",
        "is_siliconflow_endpoint",
        "normalize_model_for_endpoint",
        "strip_native_resource_prefix",
    )
    for name in public_names:
        assert getattr(legacy, name) is getattr(provider_detect, name)

    assert provider_detect.endpoint_hostname("HTTPS://API.SILICONFLOW.CN./v1") == (
        "api.siliconflow.cn"
    )
    assert provider_detect.normalize_model_for_endpoint(
        "models/gemini-embedding-001",
        "https://generativelanguage.googleapis.com/v1beta/openai/",
    ) == "gemini-embedding-001"


def test_public_origin_legacy_imports_are_canonical_functions():
    import public_origin as legacy
    from ombrebrain.security import public_origin

    for name in (
        "configured_public_origin",
        "normalize_http_resource",
        "normalize_public_origin",
    ):
        assert getattr(legacy, name) is getattr(public_origin, name)

    assert legacy.MAX_PUBLIC_URI_CHARS == public_origin.MAX_PUBLIC_URI_CHARS
    assert public_origin.normalize_public_origin(
        "HTTPS://Example.COM:443/mcp/"
    ) == "https://example.com"
    assert public_origin.normalize_public_origin(
        "https://user:secret@example.com/mcp"
    ) == ""


def test_bucket_scoring_legacy_imports_are_canonical_functions():
    import bucket_scoring as legacy
    from ombrebrain.retrieval import bucket_scoring

    for name in (
        "calc_emotion_score",
        "calc_time_score",
        "calc_topic_score",
        "calc_touch_score",
    ):
        assert getattr(legacy, name) is getattr(bucket_scoring, name)

    assert legacy.TIME_DECAY_LAMBDA == bucket_scoring.TIME_DECAY_LAMBDA
    assert bucket_scoring.calc_touch_score({"activation_count": 5}) == 0.5
    assert bucket_scoring.calc_emotion_score(None, None, {}) == 0.5
    assert 0.0 <= bucket_scoring.calc_topic_score(
        "memory",
        {"metadata": {"name": "memory"}, "content": "body"},
    ) <= 1.0


def test_media_store_legacy_imports_are_canonical_classes():
    import media_store as legacy
    from ombrebrain.storage import media_store

    assert legacy.MediaStore is media_store.MediaStore
    assert legacy.MediaPersistenceError is media_store.MediaPersistenceError
