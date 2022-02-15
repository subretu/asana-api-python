# asana-api-python

## 概要
- AsanaAPIのPythonラッパー。
- 公式のAPIリファレンスは下記を参照。
  - https://developers.asana.com/docs/asana

## パッケージインストール
- pipを使ったパッケージのローカルインストールが可能。
- 手順は下記の通り。
1. リポジトリのgit cloneを行う。
2. 下記コマンドを実行する
  ```zsh
  # 実行例はパッケージの場所を相対パスで記載しているが絶対パスでも可
  pip install ./asana-api-python/
  ```

## サンプルケース
- プロジェクトからタスク一覧を抽出

```python
from asana import asana

asana_api = asana.GetTasks("AsanaAPIKey")

# 引数：プロジェクトID、パラメータを含んだパス
task_data = asana_api.tasks_for_project(1234567890123456, "opt_fields=completed,name")
```

- プロジェクトから期限超過タスクを抽出

```python
from asana import asana

asana_api = asana.GetTasks("AsanaAPIKey")

# 引数：プロジェクトID
task_data = asana_api.overdue_tasks_for_project(1234567890123456)
```
- プロジェクトからセクション一覧を抽出

```python
from asana import asana

asana_api = asana.GetSections("AsanaAPIKey")

# 引数：プロジェクトID
task_data = asana_api.sections_for_project(1234567890123456)
```

- プロジェクトから完了タスク数を抽出

```python
from asana import asana

asana_api = asana.GetCount("AsanaAPIKey")

# 引数：プロジェクトID
task_data = asana_api.completed_tasks_for_project(1234567890123456)
```


