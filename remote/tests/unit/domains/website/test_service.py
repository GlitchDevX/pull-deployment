import pytest
from coveo_ref import ref
from fastapi import HTTPException
from pytest_mock import MockerFixture

from domains.website.internal import service
from domains.website.internal.service import deploy_website
from domains.website.internal.models import Deployment, WebsiteBody


@pytest.fixture
def mock_load_config(mocker: MockerFixture):
    mock = mocker.patch(*ref(service.load_config, context=service.deploy_website))
    mock.return_value.deployments = [
        Deployment(
            id="example-deployment",
            secret="example-secret",
            remote="github.com/glitchdevx/custos",
            access_token="secret_gh_token",
            target_dir="var/www/custos/html"
        )
    ]
    return mock

def test_should_deploy_website(mock_load_config):
    pass

def test_should_handle_invalid_secret(mock_load_config):
    given_input = WebsiteBody(
        deployment_id="example-deployment",
        deployment_secret="wrong-secret",
        branch_name="main",
        commit_sha="some-sha"
    )

    with pytest.raises(HTTPException) as err:
        deploy_website(given_input)

    assert err.value.status_code == 403

def test_should_handle_invalid_website_response(mock_load_config):
    given_input = WebsiteBody(
        deployment_id="non-existent-deployment",
        deployment_secret="example-secret",
        branch_name="main",
        commit_sha="some-sha"
    )

    with pytest.raises(HTTPException) as err:
        deploy_website(given_input)

    assert err.value.status_code == 403
