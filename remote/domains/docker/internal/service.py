from fastapi.exceptions import HTTPException
from python_on_whales import DockerClient

from domains.docker.internal.config import load_config
from domains.docker.internal.models import DockerBody, DockerResponse, Deployment


def deploy_compose(inputs: DockerBody):
    deployment = _get_deployment_by_id(inputs.deployment_id)
    if not deployment or deployment.secret != inputs.deployment_secret:
        raise HTTPException(status_code=403)

    docker = DockerClient(compose_files=[deployment.target_dir])

    docker.compose.pull()
    docker.compose.restart()

    return DockerResponse(result="success")


def _get_deployment_by_id(deployment_id: str) -> Deployment | None:
  all_deployments = load_config().deployments

  return next((deployment for deployment in all_deployments if deployment.id == deployment_id), None)
