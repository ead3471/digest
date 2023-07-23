from datetime import datetime

from fastapi import status
from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy.orm.session import Session

from app.models.posts import Post, Source, Subscription, Tag
from app.models.users import User
from app.schemas.posts_schemas import DigestReadSchema, PostReadSchema
from app.tests.conftest import test_app, testing_session

# client = TestClient(app)


@fixture()
def users(testing_session: Session) -> list[User]:
    users = [User(name="1"), User(name="2"), User(name="3")]
    for user in users:
        testing_session.add(user)
    testing_session.commit()
    return users


@fixture()
def tags(testing_session: Session) -> list[Tag]:
    tags = [Tag(name="1"), Tag(name="2"), Tag(name="3")]
    for tag in tags:
        testing_session.add(tag)
    testing_session.commit()
    return tags


@fixture()
def sources(testing_session: Session) -> list[Source]:
    sources = [Source(name="1"), Source(name="2"), Source(name="3")]
    for source in sources:
        testing_session.add(source)
    testing_session.commit()
    return sources


@fixture()
def posts(
    testing_session: Session, sources: list[Source], tags: list[Tag]
) -> list[Post]:
    post_1 = Post(
        text="post 1",
        created=datetime.now(),
        source_id=sources[0].id,
        score=1,
    )
    testing_session.add(post_1)
    post_1.tags.append(tags[0])
    post_1.tags.append(tags[1])

    post_2 = Post(
        text="post 2",
        created=datetime.now(),
        source_id=sources[1].id,
        score=2,
    )
    testing_session.add(post_2)
    post_2.tags.append(tags[1])

    post_3 = Post(
        text="post 3",
        created=datetime.now(),
        source_id=sources[2].id,
        score=2,
    )
    testing_session.add(post_3)
    post_3.tags.append(tags[2])

    post_4 = Post(
        text="post 4",
        created=datetime.now(),
        source_id=sources[1].id,
        score=2,
    )
    testing_session.add(post_4)
    post_4.tags.append(tags[2])

    testing_session.commit()
    return [post_1, post_2, post_3, post_4]


def test_digest_for_no_subscribed_user(
    users: list[User],
    test_app: TestClient,
):
    for user in users:
        response = test_app.get(f"/api/user/{user.id}/digest")
        digest = DigestReadSchema.parse_raw(response.text)
        assert (
            response.status_code == status.HTTP_201_CREATED
        ), "Wrong response status code"
        assert digest.user.id == user.id, "Wrong response user id"
        assert (
            len(digest.posts) == 0
        ), "The response must not contain any posts"


def test_digests_for_user_filter_by_tag(
    testing_session: Session,
    users: list[User],
    sources: list[Source],
    tags: list[Tag],
    posts: list[Post],
    test_app: TestClient,
):
    user = users[0]
    subscription_1 = Subscription(
        user_id=user.id, source_id=sources[0].id, minimum_score=1
    )
    testing_session.add(subscription_1)
    subscription_1.tags.append(tags[0])
    subscription_1.tags.append(tags[1])

    testing_session.commit()

    response = test_app.get(f"/api/user/{user.id}/digest")
    response_digest = DigestReadSchema.parse_raw(response.text)
    assert (
        response.status_code == status.HTTP_201_CREATED
    ), "Wrong response status"
    assert response_digest.user.id == user.id
    assert response_digest.user.name == user.name
    assert len(response_digest.posts) == 1
    assert response_digest.posts[0].id == posts[0].id


def test_digests_for_user_filter_by_score(
    testing_session: Session,
    users: list[User],
    sources: list[Source],
    tags: list[Tag],
    test_app: TestClient,
):
    user = users[0]
    subscription_1 = Subscription(
        user_id=user.id, source_id=sources[0].id, minimum_score=2
    )
    testing_session.add(subscription_1)
    subscription_1.tags.append(tags[0])

    testing_session.commit()

    response = test_app.get(f"/api/user/{user.id}/digest")
    response_digest = DigestReadSchema.parse_raw(response.text)
    assert (
        response.status_code == status.HTTP_201_CREATED
    ), "Wrong response status"
    assert response_digest.user.id == user.id
    assert response_digest.user.name == user.name
    assert len(response_digest.posts) == 0


def test_digests_for_user_filter_by_source(
    testing_session: Session,
    users: list[User],
    sources: list[Source],
    tags: list[Tag],
    posts: list[Post],
    test_app: TestClient,
):
    user = users[0]
    subscription_1 = Subscription(
        user_id=user.id, source_id=sources[1].id, minimum_score=1
    )
    testing_session.add(subscription_1)
    subscription_1.tags.append(tags[0])

    testing_session.commit()

    response = test_app.get(f"/api/user/{user.id}/digest")
    response_digest = DigestReadSchema.parse_raw(response.text)
    assert (
        response.status_code == status.HTTP_201_CREATED
    ), "Wrong response status"
    assert response_digest.user.id == user.id
    assert response_digest.user.name == user.name
    assert len(response_digest.posts) == 0


def test_multiple_subscription(
    testing_session: Session,
    test_app: TestClient,
    users: list[User],
    tags: list[Tag],
    sources: list[Source],
    posts: list[Post],
):
    user = users[0]
    subscription_1 = Subscription(
        user_id=user.id, source_id=sources[0].id, minimum_score=1
    )
    testing_session.add(subscription_1)
    subscription_1.tags.extend([tags[0]])

    subscription_2 = Subscription(
        user_id=user.id, source_id=sources[1].id, minimum_score=1
    )
    testing_session.add(subscription_2)
    subscription_2.tags.append(tags[2])

    testing_session.commit()

    response = test_app.get(f"/api/user/{user.id}/digest")
    response_digest = DigestReadSchema.parse_raw(response.text)
    assert (
        response.status_code == status.HTTP_201_CREATED
    ), "Wrong response status"
    response_digest = DigestReadSchema.parse_raw(response.text)
    assert len(response_digest.posts) == 2, "Wrong digest posts count"
    post_1_schema = PostReadSchema.from_orm(posts[0])
    post_2_schema = PostReadSchema.from_orm(posts[3])

    assert post_1_schema in response_digest.posts
    assert post_2_schema in response_digest.posts
