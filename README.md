# Website Pull Deployment

This tool allows you, to deploy your web-apps on any webserver
without directly connecting to the webserver.


## How it works

1. The client (CI) will create a temporary branch with the web-app you want to deploy
2. Then call the webhook on the remote server you want to deploy to
3. The remote will pull the temporary branch to the configured target dir
4. The client will delete the temporary branch

## Setup

