from pydantic import BaseModel


class UserRouterSettings(BaseModel):
    prefix: str = "/users"
    tags: list[str] = ["Пользователи"]


router_settings = UserRouterSettings()
