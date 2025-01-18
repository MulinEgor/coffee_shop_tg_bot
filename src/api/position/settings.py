from pydantic import BaseModel


class PositionRouterSettings(BaseModel):
    prefix: str = "/positions"
    tags: list[str] = ["Позиции"]
    

router_settings = PositionRouterSettings()
