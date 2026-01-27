import tempfile
from unittest.mock import MagicMock

from domains.website.models import Deployment
import pytest
from domains.website.git import pull_temp_branch
from pytest_mock import MockerFixture

@pytest.fixture
def mock_subprocess(mocker: MockerFixture):
    mock = mocker.patch("subprocess.run")
    mock.return_value.returncode = 0
    return mock

@pytest.fixture(autouse=True)
def mock_rmtree(mocker: MockerFixture):
    return mocker.patch("shutil.rmtree")

@pytest.fixture(autouse=True)
def mock_copytree(mocker: MockerFixture):
    return mocker.patch("shutil.copytree")

TMP_TEST_DIR = "/tmp/test_dir"
@pytest.fixture(autouse=True)
def mock_tmp_dir(mocker: MockerFixture):
    mock = mocker.patch("tempfile.TemporaryDirectory")
    mock.return_value = mocker.Mock(
        __enter__=mocker.Mock(return_value=TMP_TEST_DIR),
        __exit__=mocker.Mock()
    )

    return mock

@pytest.fixture
def deployment_stub():
    return Deployment(
        id="test-deployment-id",
        secret="ultra-secret-test-secret",
        remote="github.com/torvalds/linux",
        target_dir="tests/linux"
    )


def test_pull_temp_branch(mock_subprocess, deployment_stub, mock_tmp_dir, mock_copytree, mock_rmtree):
    given_branch_name = "example-deployment-1234"

    pull_temp_branch(given_branch_name, deployment_stub)

    expected_args = ["git", "clone", "-b", given_branch_name, "--depth", "1", "https://github.com/torvalds/linux", "."]
    mock_subprocess.assert_called_once_with(expected_args, cwd=TMP_TEST_DIR)
    # mock_rmtree.assert_called_once_with(TMP_TEST_DIR + "/.git")
    # mock_copytree.assert_called_once_with(TMP_TEST_DIR, deployment_stub.target_dir)
