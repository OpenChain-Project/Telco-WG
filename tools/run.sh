#!/bin/bash
set -x
CONTAINER_CMD=""

if which docker 2> /dev/null; then
    CONTAINER_CMD="docker"
elif which podman 2> /dev/null; then
    CONTAINER_CMD="podman"
else
    echo "No docker or podman runtime found, terminating."
    exit
fi

if [[ "$CONTAINER_CMD" == *"docker"* ]]; then
	DOCKER_SUDO="sudo -E"
fi

FILE=$(realpath $1)
DIR=$(dirname $FILE)
FILENAME=$(basename $FILE)

$DOCKER_SUDO $CONTAINER_CMD run --rm -v $DIR:/input openchain-telco-sbom-validator:latest /input/$FILENAME
