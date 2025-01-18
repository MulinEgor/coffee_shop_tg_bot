from pydantic import BaseModel


class PositionRouterSettings(BaseModel):
    prefix: str = "/position"
    tags: list[str] = ["Позиции"]
    

router_settings = PositionRouterSettings()
