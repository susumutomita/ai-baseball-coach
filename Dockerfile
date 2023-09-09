# Minicondaを基本イメージとして使用
FROM continuumio/miniconda3

# 必要なパッケージをインストールし、NodeSource GPGキーを追加
RUN apt-get update && \
  apt-get install -y ca-certificates curl gnupg && \
  apt-get update && \
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
RUN pip install .
