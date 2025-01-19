from sqlalchemy import Select, delete, insert, select, update
from sqlalchemy.orm import joinedload

from src.core.db import get_db_session
from src.core.order.models import Order, OrderPosition
from src.core.order.schemas import OrderCreateSchema, OrderUpdateSchema
from src.core.position.models import Position
from src.core.repository import Repository


class OrderRepository(Repository[Order, OrderCreateSchema, OrderUpdateSchema]):
    """
    Репозиторий для заказов.
    """

    def __init__(self):
        super().__init__(Order)

    async def create(self, data: OrderCreateSchema, include_related: bool) -> Order:
        """
        Создание заказа.

        Аргументы:
            data: Данные для создания заказа
            include_related: Загружать ли связанные объекты
        """
        async with get_db_session() as session:
            # Создание заказа
            stmt = insert(Order).values(
                user_id=data.user_id,
                obtaining_method=data.obtaining_method,
            )
            id = (await session.execute(stmt)).inserted_primary_key[0]

            # Создание позиций в заказе
            order_positions_data = [
                {
                    "order_id": id,
                    "position_id": order_position.position_id,
                    "quantity": order_position.quantity,
                    "weight": order_position.weight,
                }
                for order_position in data.order_positions
            ]
            stmt = insert(OrderPosition).values(order_positions_data)
            await session.execute(stmt)

            await session.commit()

            # Получение заказа с позициями
            stmt = select(Order).where(Order.id == id)
            if include_related:
                stmt = self._include_related(stmt)

            order = await session.execute(stmt)

            return order.unique().scalar_one()

    async def update(
        self, id: int, data: OrderUpdateSchema, include_related: bool
    ) -> Order:
        """
        Обновление заказа.

        Аргументы:
            id: ID заказа
            data: Данные для обновления заказа
            include_related: Загружать ли связанные объекты
        """
        async with get_db_session() as session:
            order_data = {}
            if data.user_id is not None:
                order_data["user_id"] = data.user_id
            if data.date:
                order_data["date"] = data.date
            if data.status:
                order_data["status"] = data.status
            if data.obtaining_method:
                order_data["obtaining_method"] = data.obtaining_method

            if order_data:
                stmt = update(Order).where(Order.id == id).values(order_data)
                await session.execute(stmt)

            if data.order_positions:
                # Удаление старых позиций в заказе
                stmt = delete(OrderPosition).where(OrderPosition.order_id == id)
                await session.execute(stmt)

                # Обновление позиций в заказе
                order_positions_data = [
                    {
                        "order_id": id,
                        "position_id": order_position.position_id,
                        "quantity": order_position.quantity,
                        "weight": order_position.weight,
                    }
                    for order_position in data.order_positions
                ]
                stmt = insert(OrderPosition).values(order_positions_data)
                await session.execute(stmt)
            await session.commit()

            stmt = select(Order).where(Order.id == id)
            if include_related:
                stmt = self._include_related(stmt)
            order = await session.execute(stmt)

            return order.unique().scalar_one()

    def _include_related(self, stmt: Select) -> Select:
        """
        Вспомогательная функция для включения связанных объектов.

        Аргументы:
            stmt: SQLAlchemy запрос
        """
        stmt = stmt.options(
            joinedload(self.model.order_positions)
            .joinedload(OrderPosition.position)
            .joinedload(Position.category)
        )
        return stmt
