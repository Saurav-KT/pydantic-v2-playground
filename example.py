from model import User,UserDetail, Product, UserInfo
from util import remove_empty

user = User(username="john_doe", email=None, age=30)

# email is excluded because it is None
print(user.model_dump(exclude_none=True))


# Exclude Empty Lists, Empty Strings, Empty Dicts, and None
user_detail = UserDetail(name="John", email=None, tags=[], notes="")
print(remove_empty(user_detail.model_dump()))


# Exclude fields conditionally inside the Model
p = Product(name="Laptop", price=1, discount=0, tags=[])
print(p.cleaned())

user_info= UserInfo(user_name="test_user", user_email="saurav.saurav12",tags=[])
print(user_info.model_dump())

# user_info= UserInfo(user_name="", user_email="saurav.saurav12@gmail.com", tags=["1"])
# print(user_info.model_dump())


