from pydantic import BaseModel


class CategoryCreateSchema(BaseModel):
    """
    Pydantic схема для создания категории.
    """

    name: str 


class CategoryGetSchema(CategoryCreateSchema):
    """
    Pydantic схема для получения категории.
    """

    id: int
