from .models import UserBase


def username(request):
    username = UserBase(request).user_name
    return {"username": username}
