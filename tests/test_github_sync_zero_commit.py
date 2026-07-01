import httpx
import pytest

from github_sync import GitHubSync


def _json_response(method: str, url: str, status_code: int, payload: dict) -> httpx.Response:
    return httpx.Response(
        status_code,
        json=payload,
        request=httpx.Request(method, url),
    )


@pytest.mark.asyncio
async def test_batch_commit_bootstraps_zero_commit_repository(monkeypatch):
    sync = GitHubSync(
        token="token",
        repo="owner/repo",
        branch="main",
        path_prefix="ombre",
    )
    calls: list[tuple[str, str, dict | None]] = []

    async def fake_request(_client, method: str, url: str, *, json=None, _max_retries=4):
        calls.append((method, url, json))
        if method == "GET" and url.endswith("/git/ref/heads/main"):
            return _json_response(method, url, 409, {"message": "Git Repository is empty."})
        if method == "POST" and url.endswith("/git/trees"):
            assert "base_tree" not in json
            assert json["tree"] == [
                {
                    "path": "ombre/dynamic/first.md",
                    "mode": "100644",
                    "type": "blob",
                    "content": "first memory",
                }
            ]
            return _json_response(method, url, 201, {"sha": "tree-zero"})
        if method == "POST" and url.endswith("/git/commits"):
            assert json["tree"] == "tree-zero"
            assert json["parents"] == []
            return _json_response(method, url, 201, {"sha": "commit-zero"})
        if method == "POST" and url.endswith("/git/refs"):
            assert json == {"ref": "refs/heads/main", "sha": "commit-zero"}
            return _json_response(method, url, 201, {"ref": "refs/heads/main"})
        raise AssertionError(f"Unexpected GitHub API call: {method} {url}")

    monkeypatch.setattr(sync, "_request", fake_request)

    uploaded = await sync._batch_commit({"dynamic/first.md": b"first memory"})

    assert uploaded == 1
    assert [method for method, _url, _json in calls] == ["GET", "POST", "POST", "POST"]
