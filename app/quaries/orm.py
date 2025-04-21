from sqlalchemy import select

from app.db import async_session_maker
from app.models import Worker, Resume


class AsyncOrmQueries:

    @staticmethod
    async def insert_data():
        new_worker: Worker = Worker(username='test6')
        async with async_session_maker() as ac:
            ac.add(new_worker)
            await ac.commit()

    @staticmethod
    async def select_data():
        async with async_session_maker() as ac:
            res = await ac.scalar(select(Worker).filter_by(id=1))
            print(res.username)

    @staticmethod
    async def update_data():
        async with async_session_maker() as ac:
            user: Worker = await ac.get(Worker, 1)
            user.username = 'Bob'
            await ac.commit()

    @staticmethod
    async def load_resumes():
        resumes_data: list = [
            {
                'title': 'Python Junior',
                'compensation': 50000,
                'workload': 'fulltime',
                'worker_id': 1
            },
            {
                'title': 'Python Middle',
                'compensation': 100000,
                'workload': 'fulltime',
                'worker_id': 1
            },
            {
                'title': 'QA Junior',
                'compensation': 40000,
                'workload': 'parttime',
                'worker_id': 2
            },
            {
                'title': 'QA Middle',
                'compensation': 90000,
                'workload': 'fulltime',
                'worker_id': 2
            },
        ]
        async with async_session_maker() as ac:
            resumes: list[Resume] = [Resume(**data) for data in resumes_data]
            ac.add_all(resumes)
            await ac.commit()