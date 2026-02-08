import pytest
from fastapi.exceptions import HTTPException

from domains.website.internal.config import load_config
from pytest_mock import MockerFixture


def mock_open(mocker: MockerFixture, content: str):
    mock = mocker.patch("builtins.open")
    mock.return_value.__enter__.return_value = content
    return mock

def test_should_load_config(mocker: MockerFixture):
    given_config = """
    deployments:
        - id: example-deployment
          secret: "super-secret"
          remote: "some-remote.com/1/git"
          target_dir: /var/www/example.dev/html
        - id: example-deployment-2
          secret: "super-secret-2"
          remote: "some-remote.com/2/git"
          target_dir: /var/www/v2.example.dev/html
    """.strip()
    mock_open(mocker, given_config)

    result = load_config()

    assert len(result.deployments) == 2
    assert result.deployments[0].id == "example-deployment"
    assert result.deployments[1].id == "example-deployment-2"

def test_should_handle_invalid_config(mocker: MockerFixture):
    given_config = """
    deployments:
        - id: example-deployment
          secret: "super-secret"
    """.strip()
    mock_open(mocker, given_config)

    with pytest.raises(HTTPException) as err:
        load_config()

    assert err.value.status_code == 500
    assert err.value.detail == "Could not load deployment config. See application logs for details"
