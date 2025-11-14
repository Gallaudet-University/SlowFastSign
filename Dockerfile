FROM python:3.8-slim

# Install system build dependencies for compilation
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install PyTorch
RUN pip install torch==1.13.0

# Clone ctcdecode with submodules
RUN git clone --recursive https://github.com/parlance/ctcdecode.git

WORKDIR /ctcdecode

# Install ctcdecode
RUN pip install .

# Copy the rest of your application code from /project directory
COPY . /project
WORKDIR /project
RUN pip install -r requirements.txt
