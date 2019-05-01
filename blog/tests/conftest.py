import pytest

from blog import app
from blog.tests.init_blog import init_db
from blog.common.token import Token


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    with app.app_context():
        init_db(need_confirm=False)
    yield client
    init_db(need_confirm=False)


@pytest.fixture
def register(client):
    rv = client.post('/api/v1/user/register',
                     json={'email': 'test@example.com', 'nickname': 'test'})
    ret = rv.get_json()
    Token.decode(ret['data']['token'])
    return ret['data']
