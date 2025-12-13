# Without model_rebuild(), Pydantic cannot resolve forward references.

from pydantic import BaseModel
from typing import Optional

class A(BaseModel):
    b: "B"

class B(BaseModel):
    a: A

# Try to create an instance (WILL FAIL)
# A(b={"a": {"b": None}})

A.model_rebuild()
B.model_rebuild()

A(b={"a": {"b": None}})   # Works now
