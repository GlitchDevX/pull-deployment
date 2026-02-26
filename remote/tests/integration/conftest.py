from pytest_mock import MockerFixture

def mock_builtin_open(mocker: MockerFixture, content: str):
    mock = mocker.patch("builtins.open")
    mock.return_value.__enter__.return_value = content
    return mock
