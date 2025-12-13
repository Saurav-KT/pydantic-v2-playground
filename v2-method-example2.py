# Without model_rebuild(), Pydantic cannot resolve forward references.

from pydantic import BaseModel
from typing import Optional

# Pydantic V2 forward reference example
class Department(BaseModel):
    name: str
    head: "User"

class User(BaseModel):
    name: str
    department: Department

data = {
    "name": "Engineering",
    "head": {
        "name": "Saurav",
        "department": {
            "name": "Engineering",
            "head": {
                "name": "Saurav",
                "department": None
            }
        }
    }
}
print(data)