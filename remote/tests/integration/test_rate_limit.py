import pytest
from fastapi.testclient import TestClient
from pyfakefs.fake_filesystem import FakeFilesystem

config_content = """
rate_limit:
  amount: 2
  interval_minutes: 1
deployments:
  - id: "some-project"
    secret: "some-crazy-mazy-secret"
    remote: "some-non-existent-remote"
    target_dir: "/var/www/some-project/html"
""".strip()

@pytest.fixture
def stub_website_config(fs: FakeFilesystem):
    fs.create_file("config/website.yml", contents=config_content)

@pytest.fixture
def test_client():
    from main import app
    yield TestClient(app)

def test_should_get_rate_limit(stub_website_config, test_client):
    for i in range(2):
        test_client.put("/deploy-website")

    response = test_client.put("/deploy-website")
    assert response.status_code == 429
