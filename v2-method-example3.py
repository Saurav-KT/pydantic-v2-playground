from pydantic import BaseModel, ConfigDict
from pydantic.v1 import StrictInt

"""validate_assignment=True Revalidates data on attribute assignment."""

class User(BaseModel):
    # model_config = ConfigDict(strict=True)
    model_config = ConfigDict(validate_assignment=True,
                              strict=True)
    age: int

user = User(age=20)
# user.age=30
'''
Pydantic automatically converts input values into the target type instead of rejecting them
Pydantic coerces "30" → 30
Passing a string value to an `int` field is allowed by default because Pydantic coerces it,
but enabling strict mode enforces validation and rejects such inputs.

'''
# user.age="30"

# Fails: string is not coerced to int
# User.model_validate({"age": "20"})

"""extra="allow" Allows unknown fields.
extra="forbid" Rejects unknown fields.
"""
class User(BaseModel):
    model_config = ConfigDict(extra="allow")
    # model_config = ConfigDict(extra="forbid")
    name: str


# Fails: extra field not allowed
User.model_validate({"name": "Saurav", "age": 20})

'''populate_by_name=True
Allows using field names even when aliases exist.'''

from pydantic import Field
class User(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    user_name: str = Field(alias="username")


User.model_validate({"username": "saurav"})
User.model_validate({"user_name": "saurav"})


'''frozen=True Makes the model immutable.'''

class User(BaseModel):
    model_config = ConfigDict(frozen=True)
    name: str

user = User(name="Saurav")

# user.name = "Amit"   #TypeError: model is frozen

# from_attributes=True Allows creating models from ORM / object attributes.
class ORMUser:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    age: int

orm_user = ORMUser("Saurav", 20)

user = User.model_validate(orm_user)
print(user)


# arbitrary_types_allowed=True Allows non-Pydantic / custom types.

class DatabaseConnection:
    pass

class User(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    db: DatabaseConnection

User(db=DatabaseConnection())


# Real-World FastAPI DTO Pattern
class UserCreateDTO(BaseModel):
    model_config = ConfigDict(
        strict=True,
        extra="forbid"
    )
    name: str
    age: int

class UserResponseDTO(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        frozen=True
    )
    id: int
    name: str