from pydantic import BaseModel


class CorsSettings(BaseModel):
    allow_origins: list[str] = ["*"]
    allow_credentials: bool = True
    allow_methods: list[str] = ["*"]
    allow_headers: list[str] = ["*"]


class APISettings(BaseModel):
    title: str = "API кофейни"
    root_path: str = "/api"
    docs_url: str = "/docs"
    description: str = "API для работы с кофейней"
    cors: CorsSettings = CorsSettings()


api_settings = APISettings()
