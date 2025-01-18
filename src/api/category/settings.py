from pydantic import BaseModel


class CategoryRouterSettings(BaseModel):
    prefix: str = "/categories"
    tags: list[str] = ["Категории"]
    

router_settings = CategoryRouterSettings()
