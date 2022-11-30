import pytest
import flask
from Frontend import auth
from Frontend import views
from app import app
import json


def test_base_route_success():
    with app.app_context():
        client = app.test_client()
        url = '/'

        response = client.get(url)
        # assert response.get_data() == b'Hello, World!'
        assert response.status_code == 200


def test_login_route_success():
    with app.app_context():
        client = app.test_client()
        url = '/login'

        response = client.get(url)
        # assert response.get_data() == b'Hello, World!'
        assert response.status_code == 200


def test_signup_route_success():
    with app.app_context():
        client = app.test_client()
        url = '/signup'

        response = client.get(url)
        # assert response.get_data() == b'Hello, World!'
        assert response.status_code == 200


def test_scrape_route_nologin_redirect():
    with app.app_context():
        client = app.test_client()
        url = '/scrape'

        response = client.get(url)
        # assert response.get_data() == b'Hello, World!'
        assert response.status_code == 302

