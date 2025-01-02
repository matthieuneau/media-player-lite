from sqlalchemy import create_engine

DATABASE_URL = "postgresql://my_user:my_password@localhost/postgres"
engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as connection:
        print("Database connection successful!")
except Exception as e:
    print("Database connection failed:", str(e))
