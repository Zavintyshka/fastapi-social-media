#!/bin/bash
PATH_TO_APP=
PATH_TO_SOURCE=
PROJECT_GIT_URL=https://github.com/Zavintyshka/fastapi-social-media.git
SERVICE_NAME=fastapi_server

sudo systemctl stop $SERVICE_NAME
cd $PATH_TO_APP && rm -rf source
cd $PATH_TO_APP && mkdir source
cd $PATH_TO_SOURCE && git clone $PROJECT_GIT_URL .
sudo systemctl start $SERVICE_NAME
