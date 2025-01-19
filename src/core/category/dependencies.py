from src.core.category.respository import CategoryRepository
from src.core.category.service import CategoryService
from src.core.types import ServiceException

def get_category_service(exception: Exception = ServiceException) -> CategoryService:
    return CategoryService(CategoryRepository(), exception)
