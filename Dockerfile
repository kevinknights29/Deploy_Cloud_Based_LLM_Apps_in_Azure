
FROM python:3.11.4-slim-bullseye

ENV LANG=C.UTF-8 \
    DEBIAN_FRONTEND=noninteractive

# Install packages and dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    ca-certificates \
    build-essential \
    zlib1g-dev \
    libncurses5-dev \
    libgdbm-dev \
    libnss3-dev \
    libssl-dev \
    libreadline-dev \
    libffi-dev \
    libsqlite3-dev \
    libbz2-dev \
    unzip \
    curl

# Set working directory
WORKDIR /opt/app

# Copy files
COPY .streamlit src config.yaml main.py requirements.txt install_dependencies.sh run.sh ./

# Install dependencies
RUN bash ./install_dependencies.sh ./requirements.txt && \
    rm ./install_dependencies.sh ./requirements.txt

# Run app
RUN chmod a+x run.sh
CMD ["./run.sh"]
