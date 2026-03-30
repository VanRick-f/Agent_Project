from fastapi import FastAPI,Path,Query,HTTPException,APIRouter
from pydantic import BaseModel,Field,field_validator
import re
from fastapi.responses import JSONResponse
from typing import Dict
from fastapi import Depends
from dependencies import common
'''
模块化依赖
'''
from dependencies import common
router = APIRouter(
    prefix="/item4",
    tags=["items"],
    dependencies=[Depends(common)],
    responses={404: {"description": "Not found"}},
)


fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}

@router.get("/")
async def read_items():
    return fake_items_db

@router.get("/test")
async def read_items():
    return "test ok"


@router.get("/{item_id}")
async def read_item(item_id: str):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"name": fake_items_db[item_id]["name"], "item_id": item_id}


@router.put(
    "/{item_id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_item(item_id: str):
    if item_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus"
        )
    return {"item_id": item_id, "name": "The great Plumbus"}
