# PlainSerializer lets you customize how a field is serialized without affecting how it is validated.
# It is useful when:
# You want a reusable serializer object
# You want schema-level control
# You serialize objects not validated by Pydantic fields
#You want a serializer outside of a model class

from pydantic import BaseModel, Field, field_serializer
from pydantic.functional_serializers import PlainSerializer
from pydantic import ConfigDict
from datetime import datetime

class Money:
    def __init__(self, amount: float, currency: str = "USD"):
        self.amount = amount
        self.currency = currency


# Reusable Serializer for Money
MoneySerializer = PlainSerializer(
    lambda m: {"amount": m.amount, "currency": m.currency},
    return_type=dict,
)


class Order(BaseModel):
    # custom Python types support
    model_config = ConfigDict(arbitrary_types_allowed=True)
    price: Money = Field(...)

    @field_serializer("price")
    def serialize_price(self, value: Money, _info):
        # Use the reusable serializer function
        return MoneySerializer.func(value)


order = Order(price=Money(100, "USD"))
print(order.model_dump())
print(order.model_dump_json())

class Event(BaseModel):
    name: str
    timestamp: datetime

    @field_serializer("timestamp")
    def serialize_timestamp(self, value: datetime, _info):
        return value.strftime("%d-%m-%Y")

event = Event(
    name="Product Launch",
    timestamp=datetime(2025, 1, 1)
)

print(event.model_dump_json())