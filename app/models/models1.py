import enum
from datetime import datetime

from sqlalchemy import Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.backend.db import Base
from app.models.mixins.id_mixins import IDMixin
from app.models.mixins.timestamps_mixins import TimestampsMixin


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
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    #updated_at: Mapped[datetime] = mapped_column(onupdate=datetime.now)
#
# class UserRoles(enum.Enum):
#     admin = 'admin'
#     user = 'user'
#
# class User(IDMixin, TimestampsMixin, Base):
#     __tablename__ = "users"
#
#     email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
#     password: Mapped[str] = mapped_column(String(32), nullable=False)
#     username: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
#     fullname: Mapped[str | None] = mapped_column(String(200), default=None)
#     is_active: Mapped[bool] = mapped_column(Boolean, default=True)
#     is_superuser: Mapped[bool]  = mapped_column(Boolean, default=False)
#     role: Mapped[UserRoles] = mapped_column(default=UserRoles.user)