from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean, text, ForeignKey
from sqlalchemy.dialects.postgresql.base import UUID


class Posts(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean,
                       server_default='TRUE',
                       nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False,
                        server_default=text('now()'))
    owner_id = Column(Integer,
                      ForeignKey("users.id", ondelete="CASCADE"),
                      nullable=False)

    owner = relationship("Users")


class Users(Base):
    __tablename__ = "users"

    # id: Column(UUID(as_uuid=True), primary_key=True,
    #            server_default=text("uuid_generate_v4()"))
    id = Column(Integer,
                primary_key=True,
                nullable=False)
    email = Column(String,
                   nullable=False,
                   unique=True)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False,
                        server_default=text('now()'))
    phone_mobile = Column(String,
                          nullable=True)


class Votes(Base):
    __tablename__ = "votes"

    user_id = Column(Integer,
                     ForeignKey("users.id", ondelete="CASCADE"),
                     primary_key=True)
    post_id = Column(Integer,
                     ForeignKey("posts.id", ondelete="CASCADE"),
                     primary_key=True)
