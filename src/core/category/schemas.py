from pydantic import BaseModel


class CategorySchema(BaseModel):
    """
    Pydantic схема для категории.
    """
    name: str
