import os

import aiohttp
import psycopg2
import pytest
import pytest_asyncio

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
TEST_DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost/airline"
)


def _get_test_db_conn():
    return psycopg2.connect(TEST_DATABASE_URL)


def _execute_sql_file(filename: str):
    sql_path = os.path.join(os.path.dirname(__file__), "..", "db", filename)
    with open(sql_path) as f:
        sql = f.read()
    conn = _get_test_db_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()
    finally:
        conn.close()


@pytest.fixture(scope="session", autouse=True)
def seed_db():
    _execute_sql_file("test_initial_seed.sql")
    yield
    _execute_sql_file("test_cleanup_seed.sql")


@pytest.fixture(autouse=True)
def clean_db():
    yield
    #
    _execute_sql_file("test_cleanup.sql")


@pytest_asyncio.fixture
async def client():
    async with aiohttp.ClientSession(base_url=API_BASE_URL) as session:
        yield session
