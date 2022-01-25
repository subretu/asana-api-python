# asana-api-python

## 概要
- AsanaAPIのPythonラッパー。
- 公式のAPIリファレンスは下記を参照。
  - https://developers.asana.com/docs/asana
## サンプル
- プロジェクトからタスク一覧を抽出

```python
from asana import asana

asana_api = asana.Asana("AsanaAPIKey")
# 引数：プロジェクトID、パラメータを含んだパス
task_data = asana_api.get_tasks_from_project(1234567890123456, "opt_fields=completed,name")
```
- プロジェクトからセクション一覧を抽出

```python
from asana import asana

asana_api = asana.Asana("AsanaAPIKey")
# 引数：プロジェクトID、パラメータを含んだパス
task_data = asana_api.get_tasks_from_a_section(1234567890123456, "opt_fields=name,gid")
```
  