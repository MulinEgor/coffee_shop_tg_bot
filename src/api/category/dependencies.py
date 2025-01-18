from src.core.category.respository import CategoryRepository
from src.core.category.service import CategoryService


def get_category_service() -> CategoryService:
    return CategoryService(CategoryRepository())
