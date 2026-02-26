import pytest
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from main import app
from tests.integration.conftest import mock_builtin_open

client = TestClient(app)


config_content = """
rate_limit:
  amount: 2
  interval_minutes: 1
deployments:
  - id: "some-project"
    secret: "some-crazy-mazy-secret"
    remote: "some-non-existent-remote"
    target_dir: "/var/www/some-project/html"
"""

def test_should_get_rate_limit(mocker: MockerFixture):
    mock_builtin_open(mocker, config_content)

    for i in range(10):
        print(client.put("/deploy-website"))

    response = client.put("/deploy-website")
    assert response.status_code == 429
