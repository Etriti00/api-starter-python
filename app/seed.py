"""
Database Seeder
===============
Creates initial data for development.
"""

import asyncio
from sqlalchemy import select
from app.database import async_session, create_tables
from app.models import User
from app.auth.password import hash_password


async def seed():
    """Seed the database with initial data."""
    await create_tables()

    async with async_session() as db:
        # Check if admin exists
        result = await db.execute(select(User).where(User.email == "admin@example.com"))
        if result.scalar_one_or_none():
            print("⚠️  Admin user already exists, skipping seed")
            return

        # Create admin user
        admin = User(
            email="admin@example.com",
            username="admin",
            name="Admin User",
            hashed_password=hash_password("Admin123!"),
            role="admin",
            is_active=True,
            is_superuser=True,
            email_verified=True,
        )
        db.add(admin)

        # Create test user
        test_user = User(
            email="test@example.com",
            username="testuser",
            name="Test User",
            hashed_password=hash_password("Test123!"),
            role="user",
            is_active=True,
            email_verified=True,
        )
        db.add(test_user)

        await db.commit()
        print("✅ Database seeded successfully")
        print("""
🔑 Test Credentials:
   Admin:  admin@example.com / Admin123!
   User:   test@example.com / Test123!
        """)


if __name__ == "__main__":
    asyncio.run(seed())
