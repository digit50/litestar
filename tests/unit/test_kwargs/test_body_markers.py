from typing import Any, Dict

import pytest
from typing_extensions import Annotated

from litestar import Litestar, post
from litestar.exceptions import ImproperlyConfiguredException, LitestarDeprecationWarning
from litestar.params import Body, MultipartBody


def test_deprecated_default_warns() -> None:
    @post("/")
    async def handler(data: dict = Body()) -> None:
        pass

    with pytest.raises(LitestarDeprecationWarning, match=r"Deprecated use of 'Body\(\)' as a default value"):
        Litestar([handler])


def test_body_on_top_of_marker_raises() -> None:
    @post("/")
    async def handler(
        data: Annotated[MultipartBody[Dict[str, Any]], Body(multipart_form_part_limit=1, title="T")],
    ) -> None:
        pass

    with pytest.raises(ImproperlyConfiguredException, match="more than one 'Body'"):
        Litestar([handler])
