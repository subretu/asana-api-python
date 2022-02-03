import requests
from datetime import datetime, date
import json


class AsanaBase:
    def __init__(self, apikey):
        """API実行の準備を行う。

        URL構築、APIキーの設定を行っている。

        apikey : AsanaAPIのトークン
        """
        self.asana_url = "https://app.asana.com/api"
        self.api_version = "1.0"
        self.aurl = "/".join([self.asana_url, self.api_version])
        self.apikey = apikey


class GetTasks(AsanaBase):
    def __init__(self, apikey):
        """親クラスの__init__を呼び出しを行う。

        apikey : AsanaAPIのトークン
        """
        super().__init__(apikey)

    def get_tasks_for_project(self, project_id, api_target):
        """プロジェクトからタスク一覧を返す。

        project_id : プロジェクトID
        api_target : パラメータを含んだパス
        """
        url = self.aurl + f"/projects/{project_id}/tasks/?{api_target}"
        req = requests.get(url, auth=(self.apikey, ""))
        data = req.json()

        return data

    def get_overdue_tasks_for_project(self, project_id):
        """プロジェクトから期日超過したタスクを返す。

        起点日は実行時の日付としている。

        project_id : プロジェクトID
        """
        today_date = date.today()
        overdue＿tasks = []

        url = (self.aurl + f"/projects/{project_id}/tasks/?opt_fields=due_on,name,completed")
        req = requests.get(url, auth=(self.apikey, ""))
        data = req.json()

        for i, item in enumerate(data["data"]):
            if (
                (not item["completed"])
                and (item["due_on"] is not None)
                and (datetime.strptime(item["due_on"], "%Y-%m-%d").date() < today_date)
            ):
                data = {
                    "name": item["name"],
                    "due_on": item["due_on"],
                }
                overdue＿tasks.append(data)

        return json.dumps(overdue＿tasks, ensure_ascii=False)


class GetSections(AsanaBase):
    def __init__(self, apikey):
        super().__init__(apikey)

    def get_sections_for_project(self, project_id):
        """プロジェクトからセクション一覧を返す。

        セクション一覧のIDが返り値となる。

        project_id : プロジェクトID
        """
        url = self.aurl + f"/projects/{project_id}/sections/?opt_fields=name,gid"
        req = requests.get(url, auth=(self.apikey, ""))
        data = req.json()

        return data


class GetCount(GetTasks):
    def __init__(self, apikey):
        super().__init__(apikey)

    def get_count_completed_tasks_for_project(self, project_id):
        """プロジェクトから完了タスク数を返す。

        project_id : プロジェクトID
        """
        all_task = super().get_tasks_for_project(project_id, "opt_fields=completed")
        completed_tasks_count = 0

        for i, item in enumerate(all_task["data"]):
            if item["completed"]:
                completed_tasks_count += 1

        return completed_tasks_count

    def get_count_uncompleted_tasks_for_project(self, project_id):
        """プロジェクトから未完了タスク数を返す。

        project_id : プロジェクトID
        """
        all_task = super().get_tasks_for_project(project_id, "opt_fields=completed")
        uncompleted_tasks_count = 0

        for i, item in enumerate(all_task["data"]):
            if not item["completed"]:
                uncompleted_tasks_count += 1

        return uncompleted_tasks_count
