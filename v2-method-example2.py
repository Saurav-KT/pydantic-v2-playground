from __future__ import annotations
from pydantic import BaseModel

# Pydantic V2 forward reference example.Pydantic v2  handles circular (recursive) references
# automatically in most cases
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
# print(data)


# Important Limitation (Runtime Data Cycles)
class Author(BaseModel):
    name: str
    books: List["Book"]

class Book(BaseModel):
    title: str
    author: Author

''' Pydantic can define circular schemas, but it does not allow infinite object cycles in actual 
data:'''
author = Author(name="Alice", books=[])
book = Book(title="My Book", author=author)
author.books.append(book)  #Runtime circular reference
print(author.model_dump())

# to solve forward reference
# A common approach in APIs:
from pydantic import BaseModel
from typing import List

class Book(BaseModel):
    title: str
    author_id: int

class Author(BaseModel):
    id: int
    name: str
    books: List[Book]

author = Author(id=1, name="Alice", books=[])
book = Book(title="My Book", author_id=author.id)
author.books.append(book)

print(author.model_dump())