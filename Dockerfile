# Minicondaを基本イメージとして使用
FROM continuumio/miniconda3

# 必要なパッケージをインストールし、NodeSource GPGキーを追加
RUN apt-get update && \
  apt-get install -y ca-certificates curl gnupg make && \
  mkdir -p /etc/apt/keyrings && \
  curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg

# debリポジトリを作成
RUN echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_16.x nodistro main" > /etc/apt/sources.list.d/nodesource.list

# Node.jsをインストール
RUN apt-get update && \
  apt-get install -y nodejs

# 作業ディレクトリの設定
WORKDIR /app

# environment.ymlをコンテナにコピー
COPY environment.yml .

# Conda環境を作成
RUN conda env create -f environment.yml

# Conda環境を有効化
SHELL ["conda", "run", "-n", "ai-baseballcoach", "/bin/bash", "-c"]

# アプリケーションのコードをコピー（必要に応じて）
COPY . .

# npmとpipで依存関係をインストール
RUN make install
RUN pip install .
