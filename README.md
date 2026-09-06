# Website Pull Deployment

Deploy in seconds using pull-based-deployment.

This tool allows you, to deploy your web-apps by pulling the content from a temporary git branch.

This has the benefit that you do not need to directly connect to your server therefore not sharing a private key.


## How it works

1. The client will create a temporary branch with the web-app you want to deploy
2. Then call the webhook on the remote server you want to deploy to
3. The remote will pull the temporary branch to the configured target dir
4. The client will delete the temporary branch


## Usage

```yml
- name: Deploy Website
  uses: glitchdevx/pull-deployment/client/website@main
  with:
    target-dir: dist
    deployment-id: ${{ secrets.DEPLOYMENT_ID }}
    deployment-secret: ${{ secrets.DEPLOYMENT_SECRET }}
    webhook-url: ${{ secrets.DEPLOYMENT_URL }}
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

To push the temp branch, your GitHub action token needs to have the `contents: write` permission.

```yml
permissions:
  contents: write
```


## Setup Remote

You'll need to have [Docker](https://docs.docker.com/engine/install/) installed.

1. Create a new directory on your server, for example named `pull-deployment`.
2. Inside of that directory create a file named `docker-compose.yaml` with the following content:
   ```yml
   services:
     pull-deployment:
       image: "glitchdevx/pull-deployment:latest"
       ports: ["127.0.0.1:<your-port>:8080"]
       volumes:
         - "./config:/config:ro"
         - "/var/www:/var/www"
   ```
   > [!IMPORTANT]
   > With port forwarding like this, you'll need to add [your own reverse proxy](#reverse-proxy)
   > to map the local port to a public one using HTTPS

   > [!TIP]
   > You can replace the `/var/www` volumes with more fine grained volumes for each website

3. Also inside the directory create a config file at `config/website.yml`, here you'll define
   the deployments you want. An example file for a server using nginx could look like this:
   ```yml
   deployments:
     - id: "example-app"
       secret: "SOME_ULTRA_SECRET_SECRET"
       remote: "github.com/your_username/example-app"
       access_token: "your_fine_grained_repository_read_token"
       target_dir: "/var/www/example-app/html"
   ```

   Generate a secret for the deployment, the longer the better.
   To generate a secret on Linux you can use the `openssl` cli:
   ```bash
   openssl rand -base64 96
   ```


### Reverse Proxy

As this tool is used to deploy web-apps this section will
assume you have a web server (like Nginx or Caddy) set up and running with SSL.


#### Nginx

If you use nginx you will need a config something like this:

```nginx
server {
  listen [::]:443 ssl;
  listen 443 ssl;

  server_name <your hostname>;

  location / {
    include /etc/nginx/includes/proxy.conf;
    proxy_pass http://127.0.0.1:<local pull-deployment port>;
  }
  ssl_certificate <path to cert>;
  ssl_certificate_key <path to cert key>;
}
```
