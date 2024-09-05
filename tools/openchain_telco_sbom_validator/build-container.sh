# © 2024 Nokia
# Licensed under the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0

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

$DOCKER_SUDO $CONTAINER_CMD build -t openchain-telco-sbom-validator:latest .
