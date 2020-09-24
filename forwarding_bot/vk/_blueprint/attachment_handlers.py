from asyncio import sleep
from typing import Dict, List

from vkbottle.types.objects.docs import Doc

from forwarding_bot.imports import json
from .settings import parse_mode, api_url
from .utils import Utils, BadRequestError


class AttachmentHandlers:
    @staticmethod
    async def no_attachments(session, request_params, tg_message):
        request_params["text"] = tg_message
        response = await session.get(api_url + "sendMessage", params=request_params)

        await Utils.response_check(response)

    @staticmethod
    async def one_attachment(session, request_params, attachments, tg_message):
        if attachments[0].type == "photo":
            photo = attachments[0].photo
            source = max(photo.sizes, key=lambda size: size.width)
            request_params["photo"] = source.url
            request_params["caption"] = tg_message
            response = await session.get(api_url + "sendPhoto", params=request_params)
            await Utils.response_check(response)
        else:
            doc = attachments[0].doc
            request_params["document"] = doc.url
            request_params["caption"] = tg_message
            response = await session.get(api_url + "sendDocument", params=request_params)
            if await Utils.response_check(response) is False:
                raise BadRequestError

    @staticmethod
    async def more_attachments(session, request_params, attachments, tg_message):
        media: List[Dict[str, str]] = []
        documents: List[Doc] = []
        for attach in attachments:
            if attach.type == "photo":
                photo = attach.photo
                source = max(photo.sizes, key=lambda size: size.width)
                media.append({
                    "type": attach.type,
                    "media": source.url,
                    "parse_mode": parse_mode
                })
            else:
                documents.append(attach.doc)

        if media:
            media[0]["caption"] = tg_message
            request_params["media"] = json.dumps(media)
            response = await session.get(api_url + "sendMediaGroup", params=request_params)
            await sleep(0.1)
            await Utils.response_check(response)
        if documents:
            bad_vibe = False
            if not media:
                request_params["caption"] = tg_message
                request_params["document"] = documents[0].url
                response = await session.get(api_url + "sendDocument", params=request_params)
                if await Utils.response_check(response) is False:
                    bad_vibe = True
                documents = documents[1:]
                request_params.pop("caption")
            for doc in documents:
                request_params["document"] = doc.url
                await sleep(0.3)
                response = await session.get(api_url + "sendDocument", params=request_params)
                if await Utils.response_check(response) is False:
                    bad_vibe = True
            if bad_vibe:
                raise BadRequestError
