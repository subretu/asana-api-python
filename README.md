# asana-api-python

## 概要
- AsanaAPIのPythonラッパー。
- 公式のAPIリファレンスは下記を参照。
  - https://developers.asana.com/docs/asana
## サンプル
- プロジェクトからタスク一覧を抽出

```python
from asana import asana

asana_api = asana.GetTasks("AsanaAPIKey")

# 引数：プロジェクトID、パラメータを含んだパス
task_data = asana_api.get_tasks_for_project(1234567890123456, "opt_fields=completed,name")
```

- プロジェクトから期限超過タスクを抽出

```python
from asana import asana

asana_api = asana.GetTasks("AsanaAPIKey")

# 引数：プロジェクトID
task_data = asana_api.get_overdue_tasks_for_project(1234567890123456)
```
- プロジェクトからセクション一覧を抽出

```python
from asana import asana

asana_api = asana.GetSections("AsanaAPIKey")

# 引数：プロジェクトID
task_data = asana_api.get_sections_for_project(1234567890123456)
```

- プロジェクトから完了タスク数を抽出

```python
from asana import asana

asana_api = asana.GetCount("AsanaAPIKey")

# 引数：プロジェクトID
task_data = asana_api.get_count_completed_tasks_for_project(1234567890123456)
```


