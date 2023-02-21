from __future__ import annotations

from enum import Enum
from typing import Any, List, Optional, Type, Union

from pydantic import BaseModel, Field

from steamship import MimeTypes, SteamshipError
from steamship.base.client import Client
from steamship.base.model import CamelModel
from steamship.base.request import DeleteRequest, IdentifierRequest, Request
from steamship.base.response import Response
from steamship.data.tags.tag import Tag


class BlockQueryRequest(Request):
    tag_filter_query: str


class BlockUploadType(str, Enum):
    FILE = "file"  # A file uploaded as bytes or a string
    BLOCKS = "blocks"  # Blocks are sent to create a file
    URL = "url"  # content will be fetched from a URL


class Block(CamelModel):
    client: Client = Field(None, exclude=True)
    id: str = None
    file_id: str = None
    text: str = None
    tags: Optional[List[Tag]] = []
    index_in_file: Optional[int] = Field(alias="index")
    mime_type: Optional[MimeTypes]

    class ListRequest(Request):
        file_id: str = None

    class ListResponse(Response):
        blocks: List[Block] = []

    @classmethod
    def parse_obj(cls: Type[BaseModel], obj: Any) -> BaseModel:
        # TODO (enias): This needs to be solved at the engine side
        obj = obj["block"] if "block" in obj else obj
        return super().parse_obj(obj)

    @staticmethod
    def get(
        client: Client,
        _id: str = None,
    ) -> Block:
        return client.post(
            "block/get",
            IdentifierRequest(id=_id),
            expect=Block,
        )

    @staticmethod
    def create(
        client: Client,
        file_id: str = None,
        text: str = None,
        tags: List[Tag] = None,
        content: Union[str, bytes] = None,
        url: Optional[str] = None,
        mime_type: Optional[MimeTypes] = None,
    ) -> Block:

        if content is not None and url is not None:
            raise SteamshipError("May provide content or URL, but not both when creating a Block")

        if content is not None:
            upload_type = BlockUploadType.FILE
        elif url is not None:
            upload_type = BlockUploadType.URL

        req = {
            "fileId": file_id,
            "text": text,
            "tags": tags,
            "url": url,
            "mimeType": mime_type,
            "type": upload_type,
        }

        file_data = (
            ("file-part", content, "multipart/form-data")
            if upload_type == BlockUploadType.FILE
            else None
        )

        return client.post(
            "block/create",
            req,
            expect=Block,
            file=file_data,
        )

    def delete(self) -> Block:
        return self.client.post(
            "block/delete",
            DeleteRequest(id=self.id),
            expect=Tag,
        )

    @staticmethod
    def query(
        client: Client,
        tag_filter_query: str,
    ) -> BlockQueryResponse:
        req = BlockQueryRequest(tag_filter_query=tag_filter_query)
        res = client.post(
            "block/query",
            payload=req,
            expect=BlockQueryResponse,
        )
        return res

    def index(self, embedding_plugin_instance: Any = None):
        """Index this block."""
        tags = [
            Tag(
                text=self.text,
                file_id=self.file_id,
                block_id=self.id,
                kind="block",
                start_idx=0,
                end_idx=len(self.text),
            )
        ]
        return embedding_plugin_instance.insert(tags)

    def raw(self):
        return self.client.post(
            "block/raw",
            payload={
                id: self.id,
            },
            raw_response=True,
        )


class BlockQueryResponse(Response):
    blocks: List[Block]


Block.ListResponse.update_forward_refs()
Block.update_forward_refs()
