from pydantic import BaseModel


class OrderRouterSettings(BaseModel):
    prefix: str = "/orders"
    tags: list[str] = ["Заказы"]


router_settings = OrderRouterSettings()
