import inject
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import literal_column
from sqlalchemy.engine import Connection

from hex.adapters.database.postgres import posts
from hex.application import create_application
from hex.domain.post import Post


@pytest.fixture
def client() -> TestClient:
    inject.clear()
    application = create_application()
    return TestClient(application)


@pytest.fixture
def post(database_connection: Connection) -> Post:
    insert = posts.insert().values(author_name='aaa',
                                   title='bbb',
                                   body='ccc'
                                   ).returning(literal_column('*'))
    cursor = database_connection.execute(insert)
    result = cursor.fetchone()
    return Post(**result)


class TestPosts:
    def test_post_search_searches_posts(self, client: TestClient, post: Post) -> None:
        response = client.get('/posts')

        assert response.json()['count'] == 1
        assert len(response.json()['results']) == 1
        post_response = response.json()['results'][0]
        assert post_response['id'] == post.id
        assert post_response['authorName'] == 'aaa'
        assert post_response['title'] == 'bbb'
        assert post_response['body'] == 'ccc'

    def test_post_detail(self, client: TestClient, post: Post) -> None:
        response = client.get(f'/posts/{post.id}')
        assert response.json()['id'] == post.id
        assert response.json()['authorName'] == 'aaa'
        assert response.json()['title'] == 'bbb'
        assert response.json()['body'] == 'ccc'
