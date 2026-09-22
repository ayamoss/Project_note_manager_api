def test_create_note(client):
    response = client.post('/notes', json={
        "title": "Тестовая заметка",
        "content": "Содержимое"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == "Тестовая заметка"


def test_create_note_without_title(client):
    response = client.post('/notes', json={
        "content": "Без заголовка"
    })
    assert response.status_code == 400


def test_get_notes_empty(client):
    response = client.get('/notes')
    assert response.status_code == 200
    data = response.get_json()
    assert data['total'] == 0


def test_get_notes_after_create(client):
    client.post('/notes', json={"title": "Заметка 1"})
    client.post('/notes', json={"title": "Заметка 2"})

    response = client.get('/notes')
    data = response.get_json()
    assert data['total'] == 2
    assert len(data['notes']) == 2


def test_get_single_note(client):
    create_response = client.post('/notes', json={"title": "Заметка"})
    note_id = create_response.get_json()['id']

    response = client.get(f'/notes/{note_id}')
    assert response.status_code == 200
    assert response.get_json()['title'] == "Заметка"


def test_get_nonexistent_note(client):
    response = client.get('/notes/9999')
    assert response.status_code == 404


def test_update_note(client):
    create_response = client.post('/notes', json={"title": "Старый заголовок"})
    note_id = create_response.get_json()['id']

    response = client.put(f'/notes/{note_id}', json={"title": "Новый заголовок"})
    assert response.status_code == 200
    assert response.get_json()['title'] == "Новый заголовок"


def test_delete_note(client):
    create_response = client.post('/notes', json={"title": "Удалить меня"})
    note_id = create_response.get_json()['id']

    response = client.delete(f'/notes/{note_id}')
    assert response.status_code == 204

    check_response = client.get(f'/notes/{note_id}')
    assert check_response.status_code == 404


def test_create_category(client):
    response = client.post('/categories', json={"name": "Работа"})
    assert response.status_code == 201
    assert response.get_json()['name'] == "Работа"


def test_filter_notes_by_category(client):
    cat_response = client.post('/categories', json={"name": "Работа"})
    category_id = cat_response.get_json()['id']

    client.post('/notes', json={"title": "Рабочая заметка", "category_id": category_id})
    client.post('/notes', json={"title": "Обычная заметка"})

    response = client.get('/notes?category=Работа')
    data = response.get_json()
    assert data['total'] == 1
    assert data['notes'][0]['title'] == "Рабочая заметка"


def test_pagination(client):
    for i in range(5):
        client.post('/notes', json={"title": f"Заметка {i}"})

    response = client.get('/notes?page=1&limit=2')
    data = response.get_json()
    assert len(data['notes']) == 2
    assert data['total'] == 5
    assert data['pages'] == 3