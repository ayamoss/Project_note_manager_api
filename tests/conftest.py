import pytest
from sqlalchemy.pool import StaticPool
from app import create_app, db


@pytest.fixture
def app():
    test_config = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SQLALCHEMY_ENGINE_OPTIONS': {
            'connect_args': {'check_same_thread': False},
            'poolclass': StaticPool,
        },
        'SECRET_KEY': 'test-key',
    }

    app = create_app(test_config)

    with app.app_context():
        db.create_all()   # для тестов создаём таблицы вручную

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()