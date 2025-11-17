from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List, Optional

from schemas import ContactMessage, Track, Video
from database import create_document, get_documents

app = FastAPI(title="Emberlance API", version="1.0.0")

# Allow frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["health"]) 
async def root():
    return {"status": "ok", "name": "Emberlance API"}


# Contact endpoints
@app.post("/contact", tags=["contact"]) 
async def submit_contact(payload: ContactMessage):
    doc = await create_document("contactmessage", payload.dict())
    return {"success": True, "data": doc}


# Content retrieval (public)
@app.get("/tracks", response_model=List[Track], tags=["content"]) 
async def list_tracks(published_only: bool = True, limit: int = 50):
    filt = {"published": True} if published_only else {}
    items = await get_documents("track", filt, limit)
    # Cast to Track-like dict list (ignore extra fields)
    result: List[Track] = []
    for item in items:
        result.append(Track(
            title=item.get("title"),
            description=item.get("description"),
            audio_url=item.get("audio_url"),
            video_url=item.get("video_url"),
            published=item.get("published", True),
            tags=item.get("tags")
        ))
    return result

@app.get("/videos", response_model=List[Video], tags=["content"]) 
async def list_videos(published_only: bool = True, limit: int = 50):
    filt = {"published": True} if published_only else {}
    items = await get_documents("video", filt, limit)
    result: List[Video] = []
    for item in items:
        result.append(Video(
            title=item.get("title"),
            src=item.get("src"),
            description=item.get("description"),
            published=item.get("published", True),
            tags=item.get("tags")
        ))
    return result


# Simple seeding helper (optional)
class SeedContent(BaseModel):
    tracks: Optional[List[Track]] = None
    videos: Optional[List[Video]] = None

@app.post("/seed", tags=["admin"]) 
async def seed_content(payload: SeedContent):
    created = {"tracks": 0, "videos": 0}
    if payload.tracks:
        for t in payload.tracks:
            await create_document("track", t.dict())
            created["tracks"] += 1
    if payload.videos:
        for v in payload.videos:
            await create_document("video", v.dict())
            created["videos"] += 1
    return {"success": True, "created": created}
