#!/bin/bash

HOME_PATH="/opt/codedeploy-agent/deployment-root"
SUFFIX="deployment-archive"

SERVICE="RawDataService/Service"
SERVICE_PATH="/RawDataService"
LOCAL_PREFIX="$HOME_PATH/$DEPLOYMENT_GROUP_ID/$DEPLOYMENT_ID/$SUFFIX"
CODE_PATH="$LOCAL_PREFIX/$SERVICE"

# COPY_FILES="$CODE_PATH/."

SOURCE_FILE="raw_data.py"
REQ_FILE="requirements.txt"

SOURCE_PATH="$CODE_PATH/$SOURCE_FILE"
REQ_PATH="$CODE_PATH/$REQ_FILE"
FRESH_REQ_PATH="$SERVICE_PATH/$REQ_FILE"

ARTIFACT="RawDataService.zip"
ARTIFACT_PATH="$HOME_PATH/$DEPLOYMENT_GROUP_ID/$DEPLOYMENT_ID/$SUFFIX/$ARTIFACT"

if [ ! -d "/RawDataService" ]
then
	sudo mkdir /RawDataService
fi

sudo pwd
sudo unzip -o $ARTIFACT_PATH -d $LOCAL_PREFIX

sudo cp  $SOURCE_PATH $SERVICE_PATH
sudo cp  $REQ_PATH $SERVICE_PATH

sudo pip3 install -r $FRESH_REQ_PATH
