# Ubuntuの最新版をベースにする
FROM ubuntu:latest

# 必要なパッケージのインストール
RUN apt-get update && apt-get install -y \
  wget \
  software-properties-common \
  gcc-11 \
  g++-11 \
  ca-certificates \
  curl \
  gnupg \
  make

# Python3.10を追加
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update
RUN apt-get install -y python3.10 python3-pip

# NodeSource GPGキーを追加
RUN mkdir -p /etc/apt/keyrings && \
  curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg

# debリポジトリを作成
RUN echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_16.x nodistro main" > /etc/apt/sources.list.d/nodesource.list

# Node.jsをインストール
RUN apt-get update && \
  apt-get install -y nodejs

# llama-cpp-pythonをインストール
RUN pip install llama-cpp-python

# ワークディレクトリを設定
WORKDIR /usr/src/app

# ファイルをダウンロード（必要であれば）
RUN wget https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/resolve/main/llama-2-7b-chat.ggmlv3.q8_0.bin

# アプリケーションのコードをコピー（必要であれば）
COPY . .

# npmとpipで依存関係をインストール（必要であれば）
RUN make install
RUN pip install .
