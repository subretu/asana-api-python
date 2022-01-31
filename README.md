import requests
import json


class Asana:
    def __init__(self, apikey):
        self.asana_url = "https://app.asana.com/api"
        self.api_version = "1.0"
        self.aurl = "/".join([self.asana_url, self.api_version])
        self.apikey = apikey

    def get_tasks_for_project(self, project_id, api_target):
        """
        project_id : プロジェクトID
        api_target : パラメータを含んだパス（詳細はhttps://developers.asana.com/docs/get-tasks-from-a-project参照）
        """
        url = self.aurl + f"/projects/{project_id}/tasks/?{api_target}"
        req = requests.get(url, auth=(self.apikey, ""))
        data = req.json()
        self.all_tasks_count = len(data["data"])

        return data

    def get_sections_for_project(self, project_id, api_target):
        """
        project_id : プロジェクトID
        api_target : パラメータを含んだパス（詳細はhttps://developers.asana.com/docs/get-tasks-from-a-project参照）
        """
        url = self.aurl + f"/projects/{project_id}/sections/?{api_target}"
        req = requests.get(url, auth=(self.apikey, ""))
        data = req.json()

        return data

    def get_completed_tasks_for_project_count(self, project_id):
        """
        project_id : プロジェクトID
        ※ 全タスク数とそのうちの完了タスク数を返す。
        """
        all_task = self.get_tasks_for_project(project_id, "opt_fields=completed")
        completed_tasks = 0
        for i in range(len(all_task["data"])):
            completed = all_task["data"][i]["completed"]
            if completed:
                completed_tasks += 1

        data = {
            "total": self.all_tasks_count,
            "completed": completed_tasks,
        }
        json_data = json.dumps(data)

        return json_data
