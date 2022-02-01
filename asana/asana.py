import requests
from datetime import datetime, date
import json


class Asana:
    def __init__(self, apikey):
        self.asana_url = "https://app.asana.com/api"
        self.api_version = "1.0"
        self.aurl = "/".join([self.asana_url, self.api_version])
        self.apikey = apikey

    def get_tasks_for_project(self, project_id, api_target):
        """プロジェクトのタスク一覧を返す

        param project_id: プロジェクトID
        param api_target: パラメータを含んだパス
        return data: プロジェクトのタスク全て
        """
        url = self.aurl + f"/projects/{project_id}/tasks/?{api_target}"
        req = requests.get(url, auth=(self.apikey, ""))
        data = req.json()

        return data

    def get_sections_for_project(self, project_id):
        """プロジェクトのセクション一覧を返す

        param project_id: プロジェクトID
        return data: プロジェクトのセクション全て
        """
        url = self.aurl + f"/projects/{project_id}/sections/?opt_fields=name,gid"
        req = requests.get(url, auth=(self.apikey, ""))
        data = req.json()

        return data

    def get_count_completed_tasks_for_project(self, project_id):
        """プロジェクトの完了タスク数を返す

        param project_id: プロジェクトID
        return completed_tasks_count: プロジェクトの完了タスクの合計
        """
        all_task = self.get_tasks_for_project(project_id, "opt_fields=completed")
        completed_tasks_count = 0

        for i, item in enumerate(all_task["data"]):
            if item["completed"]:
                completed_tasks_count += 1

        return completed_tasks_count

    def get_count_uncompleted_tasks_for_project(self, project_id):
        """プロジェクトの未完了タスク数を返す

        param project_id: プロジェクトID
        return completed_tasks_count: プロジェクトの未完了タスクの合計
        """
        all_task = self.get_tasks_for_project(project_id, "opt_fields=completed")
        uncompleted_tasks_count = 0

        for i, item in enumerate(all_task["data"]):
            if not item["completed"]:
                uncompleted_tasks_count += 1

        return uncompleted_tasks_count

    def get_overdue_tasks_for_project(self, project_id):
        """プロジェクトの期限超過タスクを返す

        param project_id: プロジェクトID
        return json_overdue_tasks: プロジェクトの期限超過タスク全て（json形式）
        """
        today_date = date.today()
        overdue_tasks = []

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
                overdue_tasks.append(data)

        json_overdue_tasks = json.dumps(overdue_tasks, ensure_ascii=False)

        return json_overdue_tasks
