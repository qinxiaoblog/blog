

def test_user_login(client, register):
    rv = client.post(
        '/api/v1/user/login',
        json={'email': 'test@example.com', 'password': '0123456789'})
    ret = rv.get_json()
    assert ret['err'] == 'SUCCESS'


def test_user_data(client, register):
    headers = {'User-Token': register['token']}
    rv = client.get(f'/api/v1/user/{register["userId"]}', headers=headers)
    assert rv.get_json()['data']['userId'] == 1
