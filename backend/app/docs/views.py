import os
from typing import List
from aiohttp.web import HTTPConflict
from aiohttp_apispec import (
    docs,
    request_schema,
    response_schema,
    form_schema,
)
from aiohttp.web_response import Response
from sqlalchemy import exc


from app.web.app import View
from app.web.utils import json_response
from app.docs.schemes import (
    DocsSchema,
    DocsRequestSchema,
    DocsListResponseSchema,
)
from app.docs.models import DocsBase
from app.docs.utils import GetTextContract


class DocsAddView(View):
    # @form_schema(DocsRequestSchema, put_into=None) # , locations=["files"]
    @response_schema(DocsSchema, 200)
    @docs(
        tags=["docs"],
        summary="Add files add view",
        description="Add file to database",
        consumes=["multipart/form-data"],
    )
    async def post(self) -> Response:
        reader = await self.request.multipart()

        field = await reader.next()
        assert field.name == "filename"
        name = await field.read(decode=True)

        filename = name.decode("utf-8")

        field = await reader.next()
        assert field.name == "uploaded_file"

        size = 0
        with open(os.path.join("../storage/", filename), "wb") as f:
            while True:
                chunk = await field.read_chunk()  # 8192 bytes by default.
                if not chunk:
                    break
                size += len(chunk)
                f.write(chunk)

        content = GetTextContract("../storage/" + filename)

        file = await self.store.files.create_doc(
            filename=filename, content=content, label="order"
        )

        return json_response(data=DocsSchema().dump(file))


class DocsListView(View):
    @docs(
        tags=["docs"],
        summary="Add files list view",
        description="Get list files from database",
    )
    @response_schema(DocsListResponseSchema, 200)
    async def get(self) -> Response:
        files: List[DocsBase] = await self.store.files.list_docs()
        return json_response(DocsListResponseSchema().dump({"files": files}))
