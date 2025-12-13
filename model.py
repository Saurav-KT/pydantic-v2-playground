from pydantic import BaseModel, field_validator, Field


class User(BaseModel):
    username: str= Field(min_length=1)
    email: str | None = None
    age: int | None = None

    @field_validator("age", mode="wrap")
    def validate_age(cls, v, handler, info):
        print("Raw input:", v)

        # run Pydantic's default int validation
        validated_value = handler(v)

        print("After Pydantic validation:", validated_value)

        # Add your own rule
        if validated_value < 0:
            raise ValueError("Age cannot be negative")

        return validated_value


class UserDetail(BaseModel):
    name: str
    email: str | None = None
    tags: list[str] = []
    notes: str = ""


# Exclude fields conditionally inside the Model

class Product(BaseModel):
    name: str
    price: float
    discount: float | None = None
    tags: list[str] = []

    def cleaned(self):
        data = self.model_dump()
        # Exclude if discount = 0 or None
        if data.get("discount") in (None, 0):
            data.pop("discount", None)
        # Exclude empty list
        if not data.get("tags"):
            data.pop("tags", None)
        return data


# Pydantic’s validator to remove values before output

class UserInfo(BaseModel):
    user_name: str | None= None
    user_email: str | None = None
    tags: list[str] | None = None

    @field_validator("tags", mode="after")
    def empty_list_to_none(cls, v):
        return v or None

    @field_validator("user_name")
    def user_name_check_empty(cls, v):
        if not v.strip():
            raise ValueError("name cannot be empty")
        return v

