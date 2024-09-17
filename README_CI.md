# Continuous integration/delivery using gitlab

## Setup server

Debian VM with nginx webserver

```
apt-get install nginx
```


SSL certificate via LetsEncrypt
```
apt-get update
apt-get install snapd
snap install core
snap refresh core
snap install --classic certbot
ln -s /snap/bin/certbot /usr/bin/certbot
certbot --nginx
```

## Define prod and review users for server deployment

```
useradd -m  -s /bin/bash gitlab-prod
useradd -m  -s /bin/bash gitlab-review
groupadd www-prod
groupadd www-review
usermod -a -G www-prod gitlab-prod
usermod -a -G www-review gitlab-review
```

### Generate ssh keys (on a private machine)
```
ssh-keygen -f id_rsa-gitlab-prod -N "" -C 'access gitlab-prod account'
ssh-keygen -f id_rsa-gitlab-review -N "" -C 'access gitlab-review account'
```

Then
- put the public keys on the server's
  authorized keys of users ``gitlab-prod`` and ``gitlab-review``
  ( ``/home/gitlab-prod/.ssh/authorized_keys``, )
- the private keys have to be stored on gitlab

## Setup deployment secret variables

Deployment is triggered when push to prod branch.

Setup these variables on Gitlab project under Settings > CI/CD > Variables:

```
DEPLOY_HOST (Variable): The production host we want to deploy to.
SSH_KNOWN_HOSTS (Variable): ~/.ssh/known_hosts lines on deployment container (Docker)
SSH_USER_DEPLOY (Variable): ``gitlab-prod``
SSH_USER_TEST (Variable): ``gitlab-review``
SSH_KEY_DEPLOY (File): deployment to prod SSH private key (copy-paste the whole key starting with -----BEGIN OPENSSH PRIVATE KEY-----\n...).
SSH_KEY_TEST (File): deployment to review SSH private key (copy-paste the whole key starting with -----BEGIN OPENSSH PRIVATE KEY-----\n...).
```

### Access to the www folders.
```
mkdir /var/www/prod
chgrp -R www-prod /var/www/prod
chmod -R 2774 /var/www/prod

mkdir /var/www/html/review
chgrp -R www-review /var/www/review
chmod -R 2774 /var/www/review
```


## Configure webserver prod and review

`/etc/nginx/sites-available/default`
```
server {
        listen 80 default_server;
        listen [::]:80 default_server;

        server_name _;
        root /var/www/prod;
        index index.html;

        location / {
            try_files $uri $uri/ =404;
            }

        location /review {
            root /var/www;
            access_log  /var/log/nginx/review.access.log;
            try_files $uri $uri/ =404;
            }
}
```
## Install gilab-runner

Enable CI on project and install gitlab-runner on a CI server.
Instructions can be found on gitlab (projet/settings/ci/runner)
https://docs.gitlab.com/runner/install/

```
apt-get update
apt-get install curl git rsync ca-certificates gnupg lsb-release
# install docker
mkdir -m 0755 -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
$(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list
> /dev/null
apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
# install gitlab-runner
curl -LJO "https://gitlab-runner-downloads.s3.amazonaws.com/latest/deb/gitlab-runner_amd64.deb"
dpkg -i gitlab-runner_amd64.deb
```

Important: on the gitlab-runner server, set a "never" pull policy,
otherwise our docker images will not be found.

In `/etc/gitlab-runner/config.toml`,
```
[[runners]]
  [runners.docker]
    pull_policy = ["never"]
```

## Build and Register Gitlab Runners

Enable CI on gitlab's project settings and
obtain the runner token from https://gitlab.math.univ-paris-diderot.fr/molin/ical-ufr/-/settings/ci_cd

```
REGISTRATION_TOKEN="<token from gitlab settings>"
```

Build docker images on CI server.

The command must be run at the top directory of the ical-ufr project
to access the config files.

```
RUNNER_IMAGE="ical-requests"
docker build -t $RUNNER_IMAGE -f ci/$RUNNER_IMAGE/Dockerfile .
```

and register with the token

```
sudo gitlab-runner register \
     --url https://gitlab.math.univ-paris-diderot.fr/ \
     --description "$RUNNER_IMAGE" \
     --tag-list "$RUNNER_IMAGE" \
     --executor "docker" \
     --docker-image "$RUNNER_IMAGE" \
     --registration-token $REGISTRATION_TOKEN
```

Do the same two steps with the webpack image
```
RUNNER_IMAGE="ical-webpack"
```

and with the rsync image
```
RUNNER_IMAGE="ical-rsync"
```

## Done

The setup is finished once the gitlab-ci.yml file is properly set
with correct "tags" options.
The deployment occurs when the ``prod`` branch is updated.
