FROM continuumio/miniconda3

RUN apt-get update && \
  apt-get install -y ca-certificates curl gnupg make software-properties-common g++-11 && \
  mkdir -p /etc/apt/keyrings && \
  curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg

RUN echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_16.x nodistro main" > /etc/apt/sources.list.d/nodesource.list

RUN apt-get update && \
  apt-get install -y nodejs

WORKDIR /app

COPY . .

RUN make install
RUN pip install .
