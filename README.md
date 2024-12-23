# WebSocketPy
PythonでのWebSocket動画サーバー with HikVision (rtsp)


## 環境作成

※Pythonあまり使わない人向け

1. Python をインストール (作成時点 3.12.7)

    適宜調べてインストールしてください。

1. 仮想環境を作成

    venvという名前のvenv(仮想環境)を作成
    ```
    python -m venv venv
    ```
1. 仮想環境をアクティベート
    
    Windows 
    ```
    myenv\Scripts\activate
    ```

    Mac/Linux
    ```
    source myenv/bin/activate
    ```

1. requirements.txt を使用してパッケージをインストール

    仮想環境がアクティブな状態で以下を実行して、requirements.txt に記載されたパッケージをインストールします：
    ```
    pip install -r requirements.txt
    ```
1. 確認

    必要なパッケージがインストールされているか確認します。

    ```
    pip list
    ```

## ソースの実行方法

1. サーバーの起動
    
    ```
    py .\websocket_server.py
    ```
1. ブラウザでの実行

    - ./web/index.html をブラウザで実行
    - ブラウザ上の


## メモ

1. 終了方法

    ```
    deactivate
    ```
1. requirements.txt の更新

    インストールした追加パッケージを含んでrequirements.txtを再作成

    ```
    pip freeze > requirements.txt
    ```