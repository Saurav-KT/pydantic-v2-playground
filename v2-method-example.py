# model_validate() Validate raw data into a model
from model import User
raw_data={
    "username":"dd",
    "email": "saurav.saurav12@gmail.com",
    "age":20

}
user = User.model_validate(raw_data, strict=True)
print("\nValidated user:", user)


# model_dump() – Convert model to Python dict
data_dict = user.model_dump()
print("\nmodel_dump():", data_dict)

# model_dump_json() – Serialize to JSON
data_json = user.model_dump_json()
print("\nmodel_dump_json():", data_json)

# model_copy() – Copy model
user_copy = user.model_copy(update={"name": "Alice Clone"})
print("\nmodel_copy():", user_copy)