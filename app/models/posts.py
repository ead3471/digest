import datetime

from sqlalchemy import (CheckConstraint, Column, DateTime, ForeignKey, Integer,
                        String, Table, Text, UniqueConstraint)
from sqlalchemy.orm import relationship

from ..database import Base

"""
    Many to many post-digest table
"""
posts_digests = Table(
    "post_digests",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id")),
    Column("digest_id", Integer, ForeignKey("digests.id")),
    UniqueConstraint("post_id", "digest_id", name="uq_posts_digests"),
)


"""
    Many to many post-tags table
"""
posts_tags = Table(
    "posts_tags",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id")),
    Column("tag_id", Integer, ForeignKey("tags.id")),
    UniqueConstraint("post_id", "tag_id", name="uq_posts_tags"),
)

"""
    Many to many subscription-tags table
"""
subscriptions_tags = Table(
    "subscriptions_tags",
    Base.metadata,
    Column("subscription_id", Integer, ForeignKey("subscriptions.id")),
    Column("tag_id", Integer, ForeignKey("tags.id")),
    UniqueConstraint(
        "subscription_id", "tag_id", name="uq_subscriptions_tags"
    ),
)


class Tag(Base):
    """Post tags"""

    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    posts = relationship(
        "Post",
        secondary=posts_tags,
        back_populates="tags",
        cascade="all, delete",
    )
    subscriptions = relationship(
        "Subscription",
        secondary=subscriptions_tags,
        back_populates="tags",
        cascade="all, delete",
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
    subscriptions = relationship(
        "Subscription", back_populates="source", cascade="all, delete"
    )

    def __repr__(self):
        return f"{self.id}:{self.name}"


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    text = Column(Text)
    score = Column(Integer, CheckConstraint("score BETWEEN 0 AND 10"))
    digests = relationship(
        "Digest", secondary=posts_digests, back_populates="posts"
    )
    tags = relationship("Tag", secondary=posts_tags, back_populates="posts")
    source_id = Column(Integer, ForeignKey("sources.id"))
    source = relationship(Source, back_populates="posts")
    created = Column(DateTime)


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
    created = Column(
        DateTime, server_default=datetime.datetime.utcnow().isoformat()
    )


class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="subscriptions")
    minimum_score = Column(Integer, default=0)
    source_id = Column(Integer, ForeignKey("sources.id"))
    source = relationship(Source, back_populates="subscriptions")
    tags = relationship(
        Tag, secondary=subscriptions_tags, back_populates="subscriptions"
    )
    __table_args__ = (
        UniqueConstraint("user_id", "source_id", name="uq_user_source"),
    )
