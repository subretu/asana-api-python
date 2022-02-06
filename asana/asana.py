import requests
from datetime import datetime, date
import json


class AsanaBase:
    def __init__(self, apikey):
        """"API実行の準備を行う。

        URL構築、APIキーの設定を行っている。

        Args:
            apikey (str): AsanaAPIのトークン
        """
        self.asana_url = "https://app.asana.com/api"
        self.api_version = "1.0"
        self.aurl = "/".join([self.asana_url, self.api_version])
        self.apikey = apikey


class GetTasks(AsanaBase):
    def __init__(self, apikey):
        """親クラスの__init__を呼び出しを行う。

        Args:
            apikey (str): AsanaAPIのトークン
        """
        super().__init__(apikey)

    def get_tasks_for_project(self, project_id, api_target):
        """プロジェクトからタスク一覧を返す。

        Args:
            project_id (int): プロジェクトID
            api_target (str): パラメータを含んだパス

        Returns:
            json: タスク一覧
        """
        url = self.aurl + f"/projects/{project_id}/tasks/?{api_target}"
        req = requests.get(url, auth=(self.apikey, ""))
        data = req.json()

        return data

    def get_overdue_tasks_for_project(self, project_id):
        """プロジェクトから期日超過したタスクを返す。

        起点日は実行時の日付としている。

        Args:
            project_id (int): プロジェクトID

        Returns:
            json: 期限超過しているタスク一覧
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
        """親クラスの__init__を呼び出しを行う。

        Args:
            apikey (str): AsanaAPIのトークン
        """
        super().__init__(apikey)

    def get_sections_for_project(self, project_id):
        """プロジェクトからセクション一覧を返す。

        起点日は実行時の日付としている。

        Args:
            project_id (int): プロジェクトID

        Returns:
            json: セクションID一覧
        """
        url = self.aurl + f"/projects/{project_id}/sections/?opt_fields=name,gid"
        req = requests.get(url, auth=(self.apikey, ""))
        data = req.json()

        return data


class GetUsers(AsanaBase):
    def __init__(self, apikey):
        super().__init__(apikey)

    def all_users_for_workspace(self, workspace_id):
        """ワークスペースの全ユーザーを返す。

        Args:
            workspace_id (int): ワークスペースID

        Returns:
            json: 全ユーザー一覧
        """
        url = self.aurl + f"/users/?opt_fields=name,gid&workspace={workspace_id}"
        req = requests.get(url, auth=(self.apikey, ""))
        data = req.json()

        return data

    def target_user_for_workspace(self, workspace_id, target_username):
        """ワークスペースの全ユーザーを返す。

        Args:
            workspace_id (int): ワークスペースID
            target_username (str): 対象ユーザーの名前

        Returns:
            json: 対象ユーザー
        """
        url = self.aurl + f"/users/?opt_fields=name,gid&workspace={workspace_id}"
        req = requests.get(url, auth=(self.apikey, ""))
        data = req.json()

        for i, item in enumerate(data["data"]):
            if item["name"] == target_username:
                return item
        else:
            return "Target username does not exist."


class GetCount(GetTasks):
    def __init__(self, apikey):
        """親クラスの__init__を呼び出しを行う。

        Args:
            apikey (str): AsanaAPIのトークン
        """
        super().__init__(apikey)

    def get_count_completed_tasks_for_project(self, project_id):
        """プロジェクトから完了タスク数を返す。

        Args:
            project_id ([int]): プロジェクトID

        Returns:
            int: 完了タスク数
        """
        all_task = super().get_tasks_for_project(project_id, "opt_fields=completed")
        completed_tasks_count = 0

        for i, item in enumerate(all_task["data"]):
            if item["completed"]:
                completed_tasks_count += 1

        return completed_tasks_count

    def get_count_uncompleted_tasks_for_project(self, project_id):
        """プロジェクトから未完了タスク数を返す。

        Args:
            project_id ([int]): プロジェクトID

        Returns:
            int: 未完了タスク数
        """
        all_task = super().get_tasks_for_project(project_id, "opt_fields=completed")
        uncompleted_tasks_count = 0

        for i, item in enumerate(all_task["data"]):
            if not item["completed"]:
                uncompleted_tasks_count += 1

        return uncompleted_tasks_count
