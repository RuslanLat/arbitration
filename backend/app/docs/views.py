import json
import os
import yaml
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
from app.mlmodel.bert_inference import run_inference
from app.mlmodel.bert_model import BertForSequenceClassification


with open("app/mlmodel/config.yml", "r") as yamlfile:
    cfg = yaml.safe_load(yamlfile)

with open("app/mlmodel/labels.json", "r", encoding="utf8") as f:
    labels = json.load(f)


model = BertForSequenceClassification(
    pretrained_model_name="DeepPavlov/rubert-base-cased",
    num_labels=cfg["model"]["num_classes"],
    dropout=cfg["model"]["dropout"],
    inference=True,
)


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

        (
            most_confident_label,
            most_confident_labels,
            getting_confidences_args,
            probabilities,
        ) = run_inference(content, "cpu", model)

        label = labels[str(most_confident_label)]

        file = await self.store.files.create_doc(
            filename=filename, content=content, label=label
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
