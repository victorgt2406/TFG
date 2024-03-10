# Python-UbuntuCUDA Docker Image

This Docker image serves as a robust foundation for applications requiring both Python and CUDA, built on top of an Ubuntu base. It integrates `pyenv` for seamless Python version management, allowing users to install different Python versions as needed.

## Docker Hub Repository

**Location:** [Python-UbuntuCUDA on Docker Hub](https://hub.docker.com/repository/docker/victorgtutad/python-ubuntucuda/general)

**Pushing a new tag:**
```
docker push victorgtutad/python-ubuntucuda:<tagname>
```

**Available Tags:**
- `3.12-ubuntu22.04`
- `3.11-ubuntu22.04`

### Tag Naming Convention
`[Python Version]-[Ubuntu Version]`

## Usage

To create a Docker image based on `Python-UbuntuCUDA`, start with the following `Dockerfile`:

```Dockerfile
FROM victorgtutad/python-ubuntucuda:3.12-ubuntu22.04
# Inherits Ubuntu 22.04 with CUDA support, enabling the use of Ubuntu commands
# Includes pyenv for Python version management

# Custom setup commands
RUN apt update
...
```

This setup ensures you have a container equipped with CUDA and your specified Python version, along with the flexibility to manage Python versions through `pyenv` and perform Ubuntu-based operations.