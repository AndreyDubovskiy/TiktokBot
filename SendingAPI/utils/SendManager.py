import SendingAPI.db.database as db
import asyncio
import httpx
import os
from typing import Any, BinaryIO

BOT_TOKEN = os.getenv("BOT_TOKEN")


class SendManager:
    def __init__(self):
        self.bot_token = BOT_TOKEN
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"

    def _build_reply_markup(self, buttons: list[dict[str, str]] | None) -> dict[str, Any] | None:
        if not buttons:
            return None
        return {
            "inline_keyboard": [[
                {
                    "text": btn["text"],
                    "callback_data": btn["callback_data"],
                }
            ] for btn in buttons]
        }

    def _file_payload(self, file_obj: BinaryIO, field_name: str) -> tuple[str, BinaryIO, str]:
        filename = os.path.basename(getattr(file_obj, "filename", "") or field_name)
        content_type = getattr(file_obj, "content_type", None) or "application/octet-stream"
        return (filename, file_obj, content_type)

    async def _send_text(
        self,
        client: httpx.AsyncClient,
        chat_id: int,
        text: str,
        buttons: list[dict[str, str]] | None = None,
        entities: list[dict[str, Any]] | None = None,
    ) -> bool:
        payload: dict[str, Any] = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
        }
        if entities:
            payload["entities"] = entities

        reply_markup = self._build_reply_markup(buttons)
        if reply_markup:
            payload["reply_markup"] = reply_markup

        res = await client.post(f"{self.base_url}/sendMessage", json=payload)
        return res.status_code == 200

    async def _send_photo(
        self,
        client: httpx.AsyncClient,
        chat_id: int,
        photo_file: BinaryIO,
        caption: str | None = None,
        buttons: list[dict[str, str]] | None = None,
        entities: list[dict[str, Any]] | None = None,
    ) -> bool:
        data: dict[str, Any] = {"chat_id": str(chat_id)}
        if caption:
            data["caption"] = caption
            data["parse_mode"] = "HTML"
        if entities:
            data["entities"] = entities

        reply_markup = self._build_reply_markup(buttons)
        if reply_markup:
            import json
            data["reply_markup"] = json.dumps(reply_markup)

        res = await client.post(
            f"{self.base_url}/sendPhoto",
            data=data,
            files={"photo": self._file_payload(photo_file, "photo")},
        )
        return res.status_code == 200

    async def _send_video(
        self,
        client: httpx.AsyncClient,
        chat_id: int,
        video_file: BinaryIO,
        caption: str | None = None,
        buttons: list[dict[str, str]] | None = None,
        entities: list[dict[str, Any]] | None = None,
    ) -> bool:
        data: dict[str, Any] = {"chat_id": str(chat_id)}
        if caption:
            data["caption"] = caption
            data["parse_mode"] = "HTML"
        if entities:
            data["entities"] = entities

        reply_markup = self._build_reply_markup(buttons)
        if reply_markup:
            import json
            data["reply_markup"] = json.dumps(reply_markup)

        res = await client.post(
            f"{self.base_url}/sendVideo",
            data=data,
            files={"video": self._file_payload(video_file, "video")},
        )
        return res.status_code == 200

    async def sent_to_one_user(self, user_id: int, text = None, photos = None, videos = None, buttons = None, entities = None) -> bool:
        photos = photos or []
        videos = videos or []
        one_photo = len(photos) == 1 and len(videos) == 0
        one_video = len(videos) == 1 and len(photos) == 0
        if one_photo:
            return await self._send_photo(
                httpx.AsyncClient(),
                user_id,
                photos[0].file,
                caption=text if text else None,
                buttons=buttons,
                entities=entities,
            )
        elif one_video:
            return await self._send_video(
                httpx.AsyncClient(),
                user_id,
                videos[0].file,
                caption=text if text else None,
                buttons=buttons,
                entities=entities,
            )
        else:
            if text or buttons:
                ok = await self._send_text(httpx.AsyncClient(), user_id, text, buttons, entities=entities)
            else:
                ok = True

            for photo_file in photos:
                ok = ok and await self._send_photo(httpx.AsyncClient(), user_id, photo_file.file, entities=entities)

            for video_file in videos:
                ok = ok and await self._send_video(httpx.AsyncClient(), user_id, video_file.file, entities=entities)

            return ok

    async def send_to_all_users(self, text = None, photos = None, videos = None, buttons = None, entities = None) -> dict[str, int]:
        offset = 0
        limit = 20
        total_sent = 0
        total_failed = 0
        while True:
            users = await db.get_all_users_new(offset=offset, limit=limit)
            if not users:
                break

            for user in users:
                ok = await self.sent_to_one_user(int(user.tg_id), text, photos, videos, buttons, entities=entities)
                if ok:
                    total_sent += 1
                else:
                    total_failed += 1
                    await db.delete_user(int(user.id))

            offset += limit
            await asyncio.sleep(1)

        return {"sent": total_sent, "failed": total_failed}


static_send_manager = SendManager()