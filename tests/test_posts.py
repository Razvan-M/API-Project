from typing import List
from venv import create
from app import schemas
import pytest


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    def validate(post):
        return schemas.PostOut(**post)
    posts_map = map(validate,res.json())

    posts_list = list(posts_map)

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_nonexistent_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{1000}")
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert res.status_code == 200
    assert post.Post.content == test_posts[0].content


@pytest.mark.parametrize("title, content, published", [("first title", "something something", True),
                                                       ("second title", "good content", False),
                                                       ("good pasta", "carbonara", True)])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post("/posts/", json= {"title" : title, "content" : content, "published" : published})

    created_post = schemas.Post(**res.json())

    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user["id"]


def test_create_default_post(authorized_client, test_user):
    res = authorized_client.post("/posts/", json= {"title" : "king of the castle", "content" : "Borat"})
    created_post = schemas.Post(**res.json())

    assert res.status_code == 201
    assert created_post.title == "king of the castle"
    assert created_post.content == "Borat"
    assert created_post.published == True
    assert created_post.owner_id == test_user["id"]


def test_unauthorized_create_post(client, test_user, test_posts):
    res = client.post("/posts/", json= {"title" : "king of the castle", "content" : "Borat"})

    assert res.status_code == 401


def test_unauthorized_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")

    assert res.status_code == 401


def test_delete_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")

    assert res.status_code == 204


def test_delete_post_nonexistent(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{1000000}")

    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")

    assert res.status_code == 403



def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title" : "updated title",
        "content" : "updated content",
        "id" : test_posts[0].id
    }

    res = authorized_client.put(f"/posts/{data['id']}", json = {"title" : data["title"], "content" : data["content"], "published" : True})

    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]


def test_update_other_user_post(authorized_client, test_user, test_posts, test_user2):
    data = {
        "title" : "updated title",
        "content" : "updated content",
        "id" : test_posts[3].id
    }

    res = authorized_client.put(f"/posts/{data['id']}", json = {"title" : data["title"], "content" : data["content"], "published" : True})

    assert res.status_code == 403


def test_unauthorized_update_post(client, test_user, test_posts):
    data = {
        "title" : "updated title",
        "content" : "updated content",
        "id" : test_posts[0].id
    }

    res = client.put(f"/posts/{data['id']}", json = {"title" : data["title"], "content" : data["content"], "published" : True})

    assert res.status_code == 401


def test_update_post_not_exist(authorized_client, test_user, test_posts):
    data = {
        "title" : "updated title",
        "content" : "updated content",
        "id" : 400000
    }

    res = authorized_client.put(f"/posts/{data['id']}", json = {"title" : data["title"], "content" : data["content"], "published" : True})

    assert res.status_code == 404