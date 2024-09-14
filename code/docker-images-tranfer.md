Script to save and load docker images from one runtime to another - courtesy ChatGPT
###### Save Images
```shell
#!/bin/bash

# Directory to save the images
SAVE_DIR="./docker_images"
mkdir -p "$SAVE_DIR"

# List all Docker images
docker image ls --format "{{.Repository}} {{.Tag}} {{.ID}}" | while read -r REPO TAG IMAGE_ID; do
  # Replace slashes in repository name with underscores
  REPO_SAFENAME=$(echo "$REPO" | sed 's/\//_/g')
  
  # Generate filename based on repository, tag, and image ID
  FILENAME="${REPO_SAFENAME}_${TAG}.tar"
  FILEPATH="${SAVE_DIR}/${FILENAME}"
  
  # Save the Docker image
  echo "Saving image ${REPO}:${TAG} as ${FILEPATH}"
  docker save -o "$FILEPATH" "$IMAGE_ID"
done
```
