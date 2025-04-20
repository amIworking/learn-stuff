import asyncio

from app.quaries.core import insert_data, create_tables

asyncio.run(create_tables())
# asyncio.run(insert_data())