import pytest
from coveo_ref import ref
from unittest.mock import MagicMock

from fastapi.exceptions import HTTPException
from domains.website.models import Deployment
from domains.website.git import pull_temp_branch
from pytest_mock import MockerFixture

from domains.website.git import subprocess, tempfile, shutil

TMP_TEST_DIR = "/tmp/test_dir"


@pytest.fixture(autouse=True)
def mock_tmp_dir(mocker: MockerFixture):
    mock = mocker.patch(*ref(tempfile.TemporaryDirectory))
    mock.return_value.__enter__.return_value = TMP_TEST_DIR
    return mock


@pytest.fixture
def mock_subprocess(mocker: MockerFixture):
    return mocker.patch(*ref(subprocess.run))


@pytest.fixture(autouse=True)
def mock_rmtree(mocker: MockerFixture):
    return mocker.patch(*ref(shutil.rmtree))


@pytest.fixture(autouse=True)
def mock_copytree(mocker: MockerFixture):
    return mocker.patch(*ref(shutil.copytree))


def build_deployment_stub(access_token: str | None = "access_token"):
    return Deployment(
        id="test-deployment-id",
        secret="ultra-secret-test-secret",
        remote="github.com/torvalds/linux",
        target_dir="tests/linux",
        access_token=access_token
    )


def test_should_pull_temp_branch_without_access_token(mocker: MockerFixture, mock_subprocess, mock_tmp_dir,
                                                      mock_copytree, mock_rmtree):
    mock_subprocess.return_value.returncode = 0
    given_branch_name = "example-deployment-1234"
    given_commit_sha = "example-commit-sha"
    given_deployment = build_deployment_stub(access_token=None)

    pull_temp_branch(given_branch_name, given_commit_sha, given_deployment)

    assert_git_subprocess_calls(mocker, mock_subprocess, given_branch_name, given_commit_sha)
    mock_rmtree.assert_called_once_with(TMP_TEST_DIR + "/.git", ignore_errors=True)
    mock_copytree.assert_called_once_with(TMP_TEST_DIR + "/.temp-deployment", given_deployment.target_dir,
                                          dirs_exist_ok=True)


def test_should_pull_temp_branch_with_access_token(mocker: MockerFixture, mock_subprocess, mock_tmp_dir, mock_copytree,
                                                   mock_rmtree):
    mock_subprocess.return_value.returncode = 0
    given_branch_name = "example-deployment-1234"
    given_commit_sha = "example-commit-sha"
    given_deployment = build_deployment_stub(access_token="access_token")

    pull_temp_branch(given_branch_name, given_commit_sha, given_deployment)

    assert_git_subprocess_calls(mocker, mock_subprocess, given_branch_name, given_commit_sha,
                                remote="https://access_token@github.com/torvalds/linux")
    mock_rmtree.assert_called_once_with(TMP_TEST_DIR + "/.git", ignore_errors=True)
    mock_copytree.assert_called_once_with(TMP_TEST_DIR + "/.temp-deployment", given_deployment.target_dir,
                                          dirs_exist_ok=True)


def test_should_handle_non_existent_branch(mocker: MockerFixture, mock_subprocess, mock_tmp_dir, mock_copytree,
                                           mock_rmtree):
    mock_subprocess.return_value.returncode = 1
    given_branch_name = "non-existent-deployment-2345"
    given_commit_sha = "example-commit-sha"
    given_deployment = build_deployment_stub(access_token=None)

    with pytest.raises(HTTPException) as err:
        pull_temp_branch(given_branch_name, given_commit_sha, given_deployment)

    assert_git_subprocess_calls(mocker, mock_subprocess, given_branch_name, given_commit_sha)
    mock_rmtree.assert_not_called()
    mock_copytree.assert_not_called()
    assert err.value.status_code == 404
    assert err.value.detail == "Temporary branch or commit sha not found"


def assert_git_subprocess_calls(mocker: MockerFixture, subprocess_mock: MagicMock, branch_name: str, commit_sha: str,
                                remote: str = "https://github.com/torvalds/linux"):
    expected_clone_args = [
        "git", "clone", "--single-branch", "-b", branch_name, "--depth", "1", remote, "."
    ]
    expected_fetch_args = ["git", "fetch", "--depth", "1", "origin", commit_sha]
    expected_checkout_args = ["git", "checkout", commit_sha]

    subprocess_mock.assert_has_calls([
        mocker.call(expected_clone_args, cwd=TMP_TEST_DIR),
        mocker.call(expected_fetch_args, cwd=TMP_TEST_DIR),
        mocker.call(expected_checkout_args, cwd=TMP_TEST_DIR),
    ], any_order=False)
