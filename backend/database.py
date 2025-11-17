import os
from typing import Any, Dict, Optional, List
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pydantic import BaseModel

MONGO_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DATABASE_NAME", "appdb")

_client: Optional[AsyncIOMotorClient] = None
_db: Optional[AsyncIOMotorDatabase] = None

async def get_db() -> AsyncIOMotorDatabase:
    global _client, _db
    if _db is None:
        _client = AsyncIOMotorClient(MONGO_URL)
        _db = _client[DB_NAME]
    return _db

async def create_document(collection: str, data: Dict[str, Any]) -> Dict[str, Any]:
    db = await get_db()
    now = datetime.utcnow()
    data_with_meta = {**data, "created_at": now, "updated_at": now}
    res = await db[collection].insert_one(data_with_meta)
    doc = await db[collection].find_one({"_id": res.inserted_id})
    if doc and "_id" in doc:
        doc["id"] = str(doc.pop("_id"))
    return doc or {}

async def get_documents(collection: str, filter_dict: Optional[Dict[str, Any]] = None, limit: int = 100) -> List[Dict[str, Any]]:
    db = await get_db()
    cur = db[collection].find(filter_dict or {}).limit(limit)
    items: List[Dict[str, Any]] = []
    async for doc in cur:
        if "_id" in doc:
            doc["id"] = str(doc.pop("_id"))
        items.append(doc)
    return items
