# ☕ Coffee shop TG bot

## 📝 Project Setup and Launch

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/).

2. Install dependencies, including dev ones:

```bash
uv sync 
```

3. Create `.env` based on `.env.example`:

```bash
cp -r src/.env.example src/.env`
```

4. Start docker container:
```bash
docker compose up -d
```

## 📁 Project structure
```
src/
├── core/       - Models pydantic и sqlalchemy, repositories and services
├── api/        - API router
├── bot/        - Tg bot logic
migrations/ - Migrations and seeds
```

## ✨ Functionality

## 🔧 Administrative Part
- Creation and editing of all entities through FastAPI
- Automatic Swagger documentation generation
- Data validation using Pydantic
- Asynchronous database operations through SQLAlchemy
- Migrations using Alembic

### 🤖 Bot
- Order creation by users
- Notifications about order status changes
- Sending notifications about new orders to baristas
- Ability for baristas to change order status through the bot
- Shopping cart for adding multiple items
- Choice of order pickup method

## 🛠 Stack
- FastAPI
- SQLAlchemy
- Alembic
- aiogram
- PostgreSQL
- Docker
- Pydantic

## 📝 Notes
- API doesn't have authentication for development simplicity. JWT authentication can be added if needed.
- All bot interactions are done through inline buttons for user convenience.
- Repository pattern is used for database operation abstraction.
- Service layer contains all business logic of the application.
