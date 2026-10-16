from typing import Any, Dict

import pytest

from litestar import Litestar, post
from litestar.exceptions import LitestarDeprecationWarning
from litestar.params import Body
from litestar.testing import TestClient


def test_deprecated_default_warns() -> None:
    @post("/")
    async def handler(data: dict = Body()) -> None:
        pass

    with pytest.raises(LitestarDeprecationWarning, match=r"Deprecated use of 'Body\(\)' as a default value"):
        Litestar([handler])


def test_deprecated_default_with_custom_media_type_warns() -> None:
    media_type = "application/vnd.api+json"

    @post("/", sync_to_thread=False)
    def handler(data: Dict[str, Any] = Body(media_type=media_type)) -> Dict[str, Any]:
        return data

    with pytest.warns(LitestarDeprecationWarning, match=r"Use 'data: Annotated\[<type>, Body\(\.\.\.\)\]'"):
        app = Litestar([handler])

    with TestClient(app) as client:
        response = client.post("/", content=b'{"a": 1}', headers={"Content-Type": media_type})

    assert response.status_code == 201
    assert response.json() == {"a": 1}
    assert list(app.openapi_schema.paths["/"].post.request_body.content) == [media_type]  # type: ignore[index, union-attr]
