#!/bin/bash

# Set the temporary directory for cloning the transformers repository
TEMP_DIR=$(mktemp -d)

# Clone the transformers repository
echo "Cloning transformers repository into ${TEMP_DIR}..."
git clone https://github.com/huggingface/transformers.git "${TEMP_DIR}"

# Check if clone was successful
if [ $? -ne 0 ]; then
    echo "Error cloning repository. Exiting."
    exit 1
fi

# Install the transformers package using pip
echo "Installing transformers from the cloned repository..."
pip install "${TEMP_DIR}"

# Check if installation was successful
if [ $? -ne 0 ]; then
    echo "Error installing transformers. Exiting."
    exit 1
fi

# Remove the temporary directory
echo "Cleaning up..."
rm -rf "${TEMP_DIR}"

echo "Installation complete."
