import requests


class Asana:

    def __init__(self, apikey):
        self.asana_url = "https://app.asana.com/api"
        self.api_version = "1.0"
        self.aurl = "/".join([self.asana_url, self.api_version])
        self.apikey = apikey

    def get_tasks_from_project(self, project_id, api_target):
        """
        project_id : プロジェクトID
        api_target : パラメータを含んだパス(詳細:https://developers.asana.com/docs/get-tasks-from-a-project)
        """
        url = self.aurl + f"/projects/{project_id}/tasks/?{api_target}"
        req = requests.get(url, auth=(self.apikey, ""))
        data = req.json()
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