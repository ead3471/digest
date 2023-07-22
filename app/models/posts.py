from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Text,
    Table,
    String,
    DateTime,
    func,
)

from ..database import Base
from sqlalchemy.orm import relationship


"""
    Many to many post-digest table
"""
posts_digests = Table(
    "post_digests",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id")),
    Column("digest_id", Integer, ForeignKey("digests.id")),
)


"""
    Many to many post-tags table
"""
posts_tags = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id")),
    Column("tag_id", Integer, ForeignKey("tags.id")),
)

"""
    Many to many subscription-tags table
"""
subscriptions_tags = Table(
    "subscriptions_tags",
    Base.metadata,
    Column("subscription_id", Integer, ForeignKey("subscriptions.id")),
    Column("tag_id", Integer, ForeignKey("tags.id")),
)


class Tag(Base):
    """Post tags"""

    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    posts = relationship("Post", back_populates="tags", cascade="all, delete")
    subscriptions = relationship(
        "Subscription", back_populates="tags", cascade="all, delete"
    )

    def __repr__(self):
        return f"{self.id}:{self.name}"


class Source(Base):
    __tablename__ = "sources"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    posts = relationship(
        "Post", back_populates="source", cascade="all, delete"
    )

    def __repr__(self):
        return f"{self.id}:{self.name}"


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False, unique=True)
    score = Column(Integer)
    digests = relationship(
        "Digest", secondary=posts_digests, back_populates="digests"
    )
    source_id = Column(Integer, ForeignKey("sources.id"))
    source = relationship(Source, back_populates="posts")
    created = Column(DateTime, default=func.now(), nullable=False)


class Digest(Base):
    __tablename__ = "digests"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="digests")
    posts = relationship(
        Post,
        secondary=posts_digests,
        back_populates="digests",
        cascade="all, delete",
    )
    tags = relationship(
        Tag, secondary=subscriptions_tags, back_populates="digests"
    )


class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="digests")
    minimum_score = Column(Integer, default=0)
    tags = relationship(
        Tag, secondary=subscriptions_tags, back_populates="subscriptions"
    )
