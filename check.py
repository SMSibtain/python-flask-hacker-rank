from email.utils import getaddresses
import functools

user = {"username": "Sibtain", "access_level": "guest"}


def make_secure(func):
    @functools.wraps(func)
    def secure_function():
        if user["access_level"] == "admin":
            return func()
        else:
            return f"No admin permissions for {user['username']}"
    return secure_function


@make_secure
def get_admin_password():
    return "1234"


print(get_admin_password())

print(4-3.14)
# from datetime import datetime
# import json


# class MyClass():
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age


# myClass = MyClass(123, datetime.fromtimestamp(1591514264000 / 1000))


# class DateTimeEncoder(json.JSONEncoder):
#     def default(self, z):
#         if isinstance(z, datetime):
#             return (str(z))
#         else:
#             return super().default(z)


# my_dict = {'date': datetime.now()}

# print(json.dumps(myClass.__dict__, cls=DateTimeEncoder))
