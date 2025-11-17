from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# Each model corresponds to a MongoDB collection named after the class, lowercased.
# e.g., ContactMessage -> collection "contactmessage"

class ContactMessage(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    email: EmailStr
    message: str = Field(..., min_length=1, max_length=5000)
    source: Optional[str] = Field(None, description="Where the message came from (page, campaign, etc.)")

class Track(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    audio_url: Optional[str] = Field(None, description="Path or URL to audio file")
    video_url: Optional[str] = Field(None, description="Path or URL to related video")
    published: bool = True
    tags: Optional[List[str]] = None

class Video(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    src: str = Field(..., description="Path or URL to the video file")
    description: Optional[str] = Field(None, max_length=1000)
    published: bool = True
    tags: Optional[List[str]] = None
