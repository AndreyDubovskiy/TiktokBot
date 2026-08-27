import asyncio
import uvicorn
import json
from io import BytesIO
from uuid import uuid4

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.encoders import jsonable_encoder
from typing import List, Optional
from utils.SendManager import static_send_manager

app = FastAPI()
broadcast_jobs = {}


async def _run_broadcast_job(
    broadcast_id: str,
    text: Optional[str],
    photos: Optional[List[UploadFile]],
    videos: Optional[List[UploadFile]],
    buttons,
    entities,
):
    try:
        result = await static_send_manager.send_to_all_users(
            text=text,
            photos=photos,
            videos=videos,
            buttons=buttons,
            entities=entities,
        )
        broadcast_jobs[broadcast_id]["status"] = "completed"
        broadcast_jobs[broadcast_id]["result"] = jsonable_encoder(result)
    except Exception as exc:
        broadcast_jobs[broadcast_id]["status"] = "failed"
        broadcast_jobs[broadcast_id]["result"] = {"error": str(exc)}
    finally:
        for files in (photos, videos):
            if not files:
                continue
            for file in files:
                await file.close()
        broadcast_jobs[broadcast_id]["task"] = None


def _serialize_broadcast_jobs():
    return {
        broadcast_id: {
            key: value
            for key, value in job_data.items()
            if key != "task"
        }
        for broadcast_id, job_data in broadcast_jobs.items()
    }


async def _freeze_uploads(files: Optional[List[UploadFile]]):
    if not files:
        return None

    frozen_files = []
    for uploaded_file in files:
        content = await uploaded_file.read()
        frozen_files.append(
            UploadFile(
                filename=uploaded_file.filename,
                file=BytesIO(content),
                headers=uploaded_file.headers,
            )
        )
        await uploaded_file.close()

    return frozen_files

@app.get("/ok")
async def ok():
    return "OK"

@app.post("/send_message/")
async def send_message(
    user_id: int = Form(None),
    text: Optional[str] = Form(None),
    photos: Optional[List[UploadFile]] = File(None),
    videos: Optional[List[UploadFile]] = File(None),
    buttons: Optional[str] = Form(None),
    entities: Optional[str] = Form(None)
):
    parsed_buttons = json.loads(buttons) if buttons else None
    parsed_entities = json.loads(entities) if entities else None
    ok = await static_send_manager.sent_to_one_user(user_id=user_id, text=text, photos=photos, videos=videos, buttons=parsed_buttons, entities=parsed_entities)
    return {"status": str(ok)}

@app.post("/send_message_to_all/")
async def send_message_to_all(
    text: Optional[str] = Form(None),
    photos: Optional[List[UploadFile]] = File(None),
    videos: Optional[List[UploadFile]] = File(None),
    buttons: Optional[str] = Form(None),
    entities: Optional[str] = Form(None)
):
    parsed_buttons = json.loads(buttons) if buttons else None
    parsed_entities = json.loads(entities) if entities else None
    frozen_photos = await _freeze_uploads(photos)
    frozen_videos = await _freeze_uploads(videos)
    broadcast_id = str(uuid4())
    task = asyncio.create_task(
        _run_broadcast_job(
            broadcast_id=broadcast_id,
            text=text,
            photos=frozen_photos,
            videos=frozen_videos,
            buttons=parsed_buttons,
            entities=parsed_entities,
        )
    )
    broadcast_jobs[broadcast_id] = {
        "status": "running",
        "result": None,
        "task": task,
    }
    return {
        "broadcast_id": broadcast_id,
        "status": "running",
    }


@app.get("/send_message_to_all_status/")
async def send_message_to_all_status():
    jobs = _serialize_broadcast_jobs()
    active_jobs = {
        broadcast_id: job_data
        for broadcast_id, job_data in jobs.items()
        if job_data["status"] == "running"
    }
    history_jobs = {
        broadcast_id: job_data
        for broadcast_id, job_data in jobs.items()
        if job_data["status"] != "running"
    }

    for broadcast_id in history_jobs:
        broadcast_jobs.pop(broadcast_id, None)

    return {
        "active": active_jobs,
        "history": history_jobs,
    }

if __name__ == "__main__":
    uvicorn.run("main:app", reload = True, port=8002)