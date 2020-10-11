import logging
from asyncio import sleep
from typing import Dict, List

from aiohttp import ClientSession
from vkbottle.types.objects.docs import Doc
from vkbottle.types.objects.messages import MessageAttachment

from forwarding_bot.imports import json
from .helpers import RequestHelper, BadDoctypeError
from .settings import parse_mode, api_url

logger = logging.getLogger("forwarding-bot")


async def no_attachments(
        session: ClientSession,
        request_params: dict,
        message_text: str
):
    logger.debug("No attachments")
    if message_text:
        logger.debug("Got text, sending")
        request_params["text"] = message_text
        response = await session.get(api_url + "sendMessage", params=request_params)

        await RequestHelper.response_check(response)
    else:
        logger.debug("No text")


async def one_attachment(
        session: ClientSession,
        request_params: dict,
        message_text: str,
        msg_attachment: MessageAttachment,
):
    logger.debug(f"One attachment with type {msg_attachment.type}")
    if msg_attachment.type == "sticker":
        request_params["text"] = message_text + "*sticker*"
        response = await session.get(api_url + "sendMessage", params=request_params)
        await RequestHelper.response_check(response)
    elif msg_attachment.type == "photo":
        photo = msg_attachment.photo
        source = max(photo.sizes, key=lambda size: size.width)
        request_params["photo"] = source.url
        request_params["caption"] = message_text
        response = await session.get(api_url + "sendPhoto", params=request_params)
        await RequestHelper.response_check(response)
    elif msg_attachment.type == "audio_message":
        voice = msg_attachment.audio_message
        request_params["caption"] = message_text
        request_params["voice"] = voice.link_ogg
        response = await session.get(api_url + "sendVoice", params=request_params)
        await RequestHelper.response_check(response)
    else:
        request_params["caption"] = message_text
        doc = msg_attachment.doc
        response = await RequestHelper.send_document(session=session,
                                                     doc=doc,
                                                     params=request_params)
        if await RequestHelper.response_check(response) is False:
            raise BadDoctypeError


async def more_attachments(
        session: ClientSession,
        request_params: dict,
        message_text: str,
        attachments: List[MessageAttachment]
):
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
        media[0]["caption"] = message_text
        request_params["media"] = json.dumps(media)
        response = await session.get(api_url + "sendMediaGroup", params=request_params)
        await sleep(0.1)
        await RequestHelper.response_check(response)
    if documents:
        bad_response = False
        if not media:
            request_params["caption"] = message_text
            doc = documents[0]
            response = await RequestHelper.send_document(session=session, doc=doc, params=request_params)
            if await RequestHelper.response_check(response) is False:
                bad_response = True
            # Cut the first document as it's already sent with caption
            documents = documents[1:]
            request_params.pop("caption")
        for doc in documents:
            await sleep(0.3)
            response = await RequestHelper.send_document(session=session, doc=doc, params=request_params)
            if await RequestHelper.response_check(response) is False:
                bad_response = True
            if await RequestHelper.response_check(response) is False:
                bad_response = True
        if bad_response:
            raise BadDoctypeError
