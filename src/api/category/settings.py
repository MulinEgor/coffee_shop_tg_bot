from pydantic import BaseModel


class CategoryRouterSettings(BaseModel):
    prefix: str = "/category"
    tags: list[str] = ["Категории"]
    

router_settings = CategoryRouterSettings()
