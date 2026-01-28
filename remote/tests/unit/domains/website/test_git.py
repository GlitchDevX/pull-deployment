from domains.website.models import Deployment
import pytest
from domains.website.git import pull_temp_branch
from pytest_mock import MockerFixture

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
def mock_subprocess_success(mocker: MockerFixture):
    return mocker.patch("subprocess.run", return_value=mocker.Mock(returncode=0))

@pytest.fixture
def mock_subprocess_fail(mocker: MockerFixture):
    return mocker.patch("subprocess.run", return_value=mocker.Mock(returncode=1))

@pytest.fixture(autouse=True)
def mock_rmtree(mocker: MockerFixture):
    return mocker.patch("shutil.rmtree")

@pytest.fixture(autouse=True)
def mock_copytree(mocker: MockerFixture):
    return mocker.patch("shutil.copytree")

@pytest.fixture
def deployment_stub():
    return Deployment(
        id="test-deployment-id",
        secret="ultra-secret-test-secret",
        remote="github.com/torvalds/linux",
        target_dir="tests/linux"
    )


def test_should_pull_temp_branch(mock_subprocess_success, deployment_stub, mock_tmp_dir, mock_copytree, mock_rmtree):
    given_branch_name = "example-deployment-1234"

    pull_temp_branch(given_branch_name, deployment_stub)

    expected_args = ["git", "clone", "-b", given_branch_name, "--depth", "1", "https://github.com/torvalds/linux", "."]
    mock_subprocess_success.assert_called_once_with(expected_args, cwd=TMP_TEST_DIR)
    mock_rmtree.assert_called_once_with(TMP_TEST_DIR + "/.git", ignore_errors=True)
    mock_copytree.assert_called_once_with(TMP_TEST_DIR, deployment_stub.target_dir, dirs_exist_ok=True)

def test_should_handle_non_existent_branch(mock_subprocess_fail, deployment_stub, mock_tmp_dir, mock_copytree, mock_rmtree):
    given_branch_name = "non-existent-deployment-2345"

    pull_temp_branch(given_branch_name, deployment_stub)

    expected_args = ["git", "clone", "-b", given_branch_name, "--depth", "1", "https://github.com/torvalds/linux", "."]
    mock_subprocess_fail.assert_called_once_with(expected_args, cwd=TMP_TEST_DIR)
    mock_rmtree.assert_not_called()
    mock_copytree.assert_not_called()
