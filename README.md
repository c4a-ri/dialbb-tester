# dialbb-tester

OpenAI ChatGPTを用いたDialBBアプリケーションのテスタ

## サンプルの動かし方

以下bashの例で説明します．

- DialBBをインストールします．

- DialBBをインストールしたディレクトリを環境変数`DIALBB_HOME`に設定します．

  ```sh
  export DIALBB_HOME=<DIALBBのインストールディレクトリ>
  ```

- 環境変数`PYTHONPATH`にDialBBのインストールディレクトリを設定します．
  
  ```sh
  export PYTHONPATH=$DIALBB_HOME:$PYTHONPATH
  ```

- Open AIのライブラリをインストールします．

  ```sh
  pip install openai
  ```

- 環境変数`OPENAI_KEY`または`OPENAI_API_KEY`にOpenAI APIのキーを設定します．

  ```sh
  export OPENAI_KEY=<OPENAIのAPIキー>
  ```

- このREADMEのあるディレクトリで以下のコマンドを実行します．

  ```sh
  python main.py --app_config $DIALBB_HOME/sample_apps/network_ja/config.yml --test_config sample_ja/config.yml --output _output.txt
  ```
  
- `_output.txt`に結果が記述されます．

## 仕様

- 起動オプション

  ```sh
  python main.py --app_config <DialBBアプリケーションのコンフィギュレーションファイル> --test_config <テストコンフィギュレーションファイル> --output <出力ファイル>
  ```
  
- テストコンフィギュレーションファイル

  以下のキーをもつYAML
  
  - `model`: （必須）OpenAIのGPTモデル名

  - `user_name`: （必須）シミュレータのキャラクタ名

  - `common_situation`: （任意）すべてのセッション共通のシチュエーション

  - `situations`: （必須）stringまたはobjectのリスト．一つの要素が一つのセッションに対応する．
  
    - stringの場合，セッション個別のシチュエーションを記述した文字列
    - objectの場合は以下のキーを持つ
      - `situation`:（必須）セッション個別のシチュエーションを記述した文字列
      - `initial_aux_data`:（任意）オブジェクト．対話開始時の`aux_data`の値．
  
  - `generation_instructions`: （必須）次発話を生成するインストラクションのリスト
  
  - `temperatures`: （任意）GPTの温度パラメータのリスト．デフォルト値は0.7の一要素のみのリスト．situationsのリストの長さ×このリストの長さのセッションが行われる．
  
    

