#!/bin/bash

# Nombre de la imagen que quieres construir
IMAGE_NAME="lsm-api"
# Tag que quieres asignar a tu imagen
TAG="v1.0"
# Nombre completo de la imagen con tag
FULL_IMAGE_NAME="${IMAGE_NAME}:${TAG}"

# Verificar si la imagen ya existe
if docker images | awk '{ print $1":"$2 }' | grep -q "^${FULL_IMAGE_NAME}$"; then
  echo "Deleting ${FULL_IMAGE_NAME} image..."
  docker rmi "${FULL_IMAGE_NAME}"
fi

# Construir la nueva imagen con el Dockerfile actual
echo "Building new image ${FULL_IMAGE_NAME} ..."
docker build -t "${FULL_IMAGE_NAME}" .

echo "Image ${FULL_IMAGE_NAME} created successfully."
