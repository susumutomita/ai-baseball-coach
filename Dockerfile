FROM continuumio/miniconda3:latest

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

RUN apt-get update && \
  apt-get install -y --no-install-recommends \
  wget \
  software-properties-common \
  ca-certificates \
  curl \
  gnupg \
  gcc \
  make && \
  rm -rf /var/lib/apt/lists/*

RUN mkdir -p /etc/apt/keyrings && \
  curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && \
  echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_16.x nodistro main" > /etc/apt/sources.list.d/nodesource.list && \
  apt-get update && \
  apt-get install -y nodejs && \
  rm -rf /var/lib/apt/lists/*

COPY . .
RUN make install

WORKDIR /app/app
CMD ["python", "main.py"]
