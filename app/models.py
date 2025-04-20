import enum
from datetime import datetime
import datetime as DT

from sqlalchemy import MetaData, Table, Integer, String, Column, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.annotation import Annotated

from app.db import Base

# metadata_obj = MetaData()
#
# workers_table = Table(
#     'workers',
#     metadata_obj,
#     Column('id', Integer, primary_key=True, autoincrement=True),
#     Column('username', String, primary_key=True)
# )
# intpk: Annotated[int] = mapped_column(Integer, primary_key=True)

class Workload(enum.Enum):
    parttime = 'parttime'
    fulltime = 'fulltime'

class Worker(Base):
    __tablename__ = 'workers'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String)


class Resume(Base):
    __tablename__ = 'resumes'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    compensation: Mapped[int | None] = mapped_column(Integer, nullable=True)
    workload: Mapped[Workload]
    worker_id: Mapped[int] = mapped_column(ForeignKey('workers.id', ondelete='CASCADE'))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(DT.UTC))
    updated_at: Mapped[datetime] = mapped_column(
        onupdate=datetime.now(DT.UTC)
    )