import gettext
from fastapi import Request

def get_locale(request: Request):
    language = request.headers.get("Accept-Language", "en")
    return language.split(",")[0]