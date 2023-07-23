from datetime import datetime
from typing import Iterable

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.posts import Digest, Post, Source, Subscription, Tag
from ..models.users import User
from ..schemas.posts_schemas import (
    DigestReadSchema,
    SubscriptionReadSchema,
    SubscriptionWriteSchema,
)
from ..schemas.users_schemas import UserBaseSchema
from .core import get_object_or_404

router = APIRouter()


@router.get(
    "/user",
    response_model=list[UserBaseSchema],
    response_description="List of users",
    status_code=status.HTTP_200_OK,
    description="Return the list of all registered users",
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
    description="Return list of subscriptions of user with given user_id",
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
    description="Generate digest for user with given user_id",
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
            for post in posts_for_subscription:
                post_tag_ids = {tag.id for tag in post.tags}
                if not post_tag_ids.isdisjoint(subscription_tag_ids):
                    new_digest.posts.append(post)

    db.commit()
    return new_digest
