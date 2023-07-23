from fastapi import APIRouter, Depends, status, HTTPException
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas.users_schemas import UserBaseSchema
from ..schemas.posts_schemas import (
    SubscriptionReadSchema,
    SubscriptionWriteSchema,
    DigestReadSchema,
    SourceReadSchema,
    SourceWriteSchema,
)
from ..models.users import User
from .core import get_object_or_404
from ..models.posts import Subscription, Tag, Source, Post, Digest
from typing import Iterable
from datetime import datetime

router = APIRouter()


@router.get(
    "/user",
    response_model=list[UserBaseSchema],
    response_description="List of users",
    status_code=status.HTTP_200_OK,
    description="Get users list",
)
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router.post(
    "/user/{user_id:int}/subscription",
    response_model=SubscriptionReadSchema,
    status_code=status.HTTP_201_CREATED,
    description="Add user subscription",
)
def create_subscription(
    user_id: int,
    subscription_data: SubscriptionWriteSchema,
    db: Session = Depends(get_db),
):
    user: User = get_object_or_404(db, User, user_id)
    data_dict = subscription_data.dict()
    tags_ids = data_dict.pop("tags")
    source_id = data_dict.pop("source")
    source: Source = get_object_or_404(db, Source, source_id)
    new_subscription = Subscription(
        user_id=user.id, source_id=source.id, **data_dict
    )
    for tag_id in tags_ids:
        tag = get_object_or_404(db, Tag, tag_id)
        new_subscription.tags.append(tag)
    db.add(new_subscription)
    db.commit()
    return new_subscription


@router.get(
    "/user/{user_id:int}/subscription",
    response_model=list[SubscriptionReadSchema],
    status_code=status.HTTP_200_OK,
    description="Get list of user subscriptions",
)
def get_subscriptions(
    user_id: int,
    db: Session = Depends(get_db),
):
    user: User = get_object_or_404(db, User, user_id)
    return user.subscriptions


@router.get(
    "/user/{user_id:int}/digest",
    response_model=DigestReadSchema,
    status_code=status.HTTP_201_CREATED,
    description="Generate user digest",
)
def generate_digest(
    user_id: int,
    db: Session = Depends(get_db),
):
    user: User = get_object_or_404(db, User, user_id)

    user_subscriptions: Iterable[Subscription] = user.subscriptions

    new_digest = Digest(user_id=user.id, created=datetime.now())
    db.add(new_digest)
    for subscription in user_subscriptions:
        posts_for_subscription = (
            db.query(Post)
            .filter(
                Post.score >= subscription.minimum_score,
                Post.source == subscription.source,
            )
            .all()
        )
        subscription_tag_ids = {tag.id for tag in subscription.tags}
        if subscription_tag_ids:
            subscription_tags_set = set(subscription.tags)
            for post in posts_for_subscription:
                post_tag_ids = {tag.id for tag in post.tags}
                if not post_tag_ids.isdisjoint(subscription_tags_set):
                    new_digest.posts.add(post)

    db.commit()
    return new_digest
