import pytest
from fastapi.exceptions import HTTPException
from pyfakefs.fake_filesystem import FakeFilesystem

from domains.website.internal.config import load_config
from pytest_mock import MockerFixture


def mock_open(mocker: MockerFixture, content: str):
    mock = mocker.patch("builtins.open")
    mock.return_value.__enter__.return_value = content
    return mock

def test_should_load_config(fs: FakeFilesystem):
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
    fs.create_file("config/valid_config", contents=given_config)

    result = load_config("config/valid_config")

    assert len(result.deployments) == 2
    assert result.deployments[0].id == "example-deployment"
    assert result.deployments[1].id == "example-deployment-2"

def test_should_handle_invalid_config(fs: FakeFilesystem):
    given_config = """
    deployments:
        - id: example-deployment
          secret: "super-secret"
    """.strip()
    fs.create_file("config/invalid_config", contents=given_config)

    with pytest.raises(HTTPException) as err:
        load_config("config/invalid_config")

    assert err.value.status_code == 500
    assert err.value.detail == "Could not load deployment config. See application logs for details"

def test_should_cache_file_load(fs: FakeFilesystem):
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
    mock_file = fs.create_file("config/cached_config", contents=given_config)

    first_result = load_config("config/cached_config")

    mock_file.set_contents("some invalid config content")
    cached_result = load_config("config/cached_config")

    assert first_result == cached_result
