from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from typing import Dict
import uvicorn
from fastapi.routing import APIRouter
from util import VersionedAPIRouter
from fastapi_versioning import VersionedFastAPI



# ------------------------------
# Pydantic v2 models
# ------------------------------
class ItemBase(BaseModel):
    name: str = Field(..., json_schema_extra={"example":"saurav"})
    qty: int= Field(...)
    price: float | None = Field(None)
    tax: float | None = Field(None)
    description: str | None= Field(None)


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: str | None = None
    qty: int = Field(...)
    price: float | None = None
    tax: float | None = None
    description: str | None = Field(None)


class Item(ItemBase):
    id: str


# ------------------------------
# In-memory “database”
# ------------------------------
items_db: Dict[str, dict] = {}

app = FastAPI(title="Versioned API")

# =====================================================
# V1 ROUTER
# =====================================================
router_v1 = VersionedAPIRouter(1, 0)

# ------------------------------
# Create (POST)
# ------------------------------
@router_v1.post("/items", response_model=Item)
async def create_item(item: ItemCreate):
    new_id = f"item{len(items_db) + 1}"
    new_item = Item(id=new_id, **item.model_dump(exclude={"tax"}))
    items_db[new_id] = jsonable_encoder(new_item)
    return new_item

# ------------------------------
# Read All (GET)
# ------------------------------

@router_v1.get("/items", response_model=list[Item], response_model_exclude_none=True)
async def list_items():
    return [Item(**data) for data in items_db.values()]

# ------------------------------
# Read One (GET)
# ------------------------------
@router_v1.get("/items/{item_id}", response_model=Item, response_model_exclude_none=True)
async def get_item(item_id: str):
    if item_id not in items_db:
        raise HTTPException(404, "Item not found")
    return Item(**items_db[item_id])


# ------------------------------
# Update (PUT) — Replace entire item
# ------------------------------
@router_v1.put("/items/{item_id}", response_model=Item)
async def replace_item(item_id: str, item: ItemCreate):
    if item_id not in items_db:
        raise HTTPException(404, "Item not found")

    replaced_item = Item(id=item_id, **item.model_dump())
    items_db[item_id] = jsonable_encoder(replaced_item)
    return replaced_item


# ------------------------------
# Partial Update (PATCH)
# ------------------------------
@router_v1.patch("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: ItemUpdate):
    if item_id not in items_db:
        raise HTTPException(404, "Item not found")

    stored = Item(**items_db[item_id])
    update_data = item.model_dump(exclude_unset=True)

    updated = stored.model_copy(update=update_data)
    items_db[item_id] = jsonable_encoder(updated)
    return updated


# ------------------------------
# Delete (DELETE)
# ------------------------------
@router_v1.delete("/items/{item_id}")
async def delete_item(item_id: str):
    if item_id not in items_db:
        raise HTTPException(404, "Item not found")

    del items_db[item_id]
    return {"message": f"Item '{item_id}' deleted successfully"}

# =====================================================
# V2 ROUTER (same behavior for now, future-ready)
# =====================================================
router_v2 = VersionedAPIRouter(2, 0)

@router_v2.get("/items", response_model=list[Item])
async def list_items_v2():
    return [Item(**data) for data in items_db.values()]

# ------------------------------
# Include Routers
# ------------------------------
app.include_router(router_v1)
app.include_router(router_v2)

# ------------------------------
# Wrap with VersionedFastAPI (LAST STEP)
# ------------------------------
app = VersionedFastAPI(
    app,
    version_format="{major}",
    prefix_format="/v{major}",
    enable_latest=True,
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8084)