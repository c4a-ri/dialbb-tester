# dialbb-tester

OpenAI ChatGPTを用いたDialBBアプリケーションのテスタ

## サンプルの動かし方

以下bashの例で説明します．

- DialBBをインストールし，[SNIPS+ネットワークベース対話管理アプリケーション](https://c4a-ri.github.io/dialbb/document-ja/build/html/03_install.html#snips)が動作することを確認します．

- DialBBをインストールしたディレクトリを環境変数`DIALBB_HOME`に設定します．

  ```sh
  export DIALBB_HOME=<DIALBBのインストールディレクトリ>
  ```

- 環境変数`PYTHONPATH`にDialBBのインストールディレクトリを設定します．
  
  ```sh
  export PYTHONPATH=$DIALBB_HOME:$PYTHONPATH
  ```

- Open AIのライブラリをインストールします。

  ```sh
  pip install openai
  ```

- 環境変数`OPENAI_KEY`にOpenAI APIのキーを設定します．

  ```sh
  export OPENAI_KEY=<OPENAIのAPIキー>
  ```

- このREADMEのあるディレクトリで以下のコマンドを実行します．

  ```sh
  python main.py --app_config $DIALBB_HOME/sample_apps/network_ja/config.yml --test_config sample_ja/config.yml --output _output.txt
  ```
  
- `_output.txt`に結果が記述されます。

## 仕様

- 起動オプション

  ```sh
  python main.py --app_config <DialBBアプリケーションのコンフィギュレーションファイル> --test_config <テストコンフィギュレーションファイル> --output <出力ファイル>
  ```
  
- テストコンフィギュレーションファイル

  以下のキーをもつYAML
  
  - `model`: OpenAIのGPTモデル名

  - `user_name`: シミュレータのキャラクタ名

  - `common_situation`: すべてのセッション共通のシチュエーション

  - `situations`: セッション個別のシチュエーションのリスト
  
  - `generation_instructions`: 次発話を生成するインストラクションのリスト

  - `temperatures`: GPTの温度パラメータのリスト
    


