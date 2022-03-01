import requests
from datetime import datetime, date


def _check_project_id(project_id):
    """プロジェクトIDのチェックを行う。

    Args:
        project_id (int): プロジェクトID

    Returns:
        boolean: 適切な入力かどうか
    """
    if (len(str(project_id)) == 16) and (type(project_id) is int):
        return True
    else:
        return False


class AsanaBase:
    def __init__(self, apikey):
        """ "API実行の準備を行う。

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

    def tasks_for_project(self, project_id, api_target):
        """プロジェクトからタスク一覧を返す。

        Args:
            project_id (int): プロジェクトID
            api_target (str): パラメータを含んだパス

        Returns:
            list: タスク一覧
        """
        try:
            if _check_project_id(project_id):
                url = (
                    self.aurl + f"/projects/{project_id}/tasks/?{api_target}&limit=100"
                )
                req = requests.get(url, auth=(self.apikey, ""))
                req.raise_for_status()
                data = req.json()
                all_data = data["data"]

                if data["next_page"] is not None:
                    api_data = data["next_page"]["offset"]
                    while api_data:
                        url = (
                            self.aurl
                            + f"/projects/{project_id}/tasks/?{api_target}&limit=100&offset={api_data}"
                        )
                        req = requests.get(url, auth=(self.apikey, ""))
                        data = req.json()
                        all_data.extend(data["data"])
                        if data["next_page"] is not None:
                            api_data = data["next_page"]["offset"]
                        else:
                            return all_data
                else:
                    return data["data"]
            else:
                raise Exception("invalid project_id")
        except Exception:
            raise

    def overdue_tasks_for_project(self, project_id, *args):
        """プロジェクトから期日超過したタスクを返す。

        デフォルトの起点日は実行時の日付としている。

        Args:
            project_id (int): プロジェクトID

        Returns:
            list: 期限超過しているタスク一覧
        """
        try:
            target_date = ""
            overdue_tasks = []

            if args:
                target_date = datetime.strptime(args[0], "%Y-%m-%d").date()
            else:
                target_date = date.today()

            all_task = self.tasks_for_project(
                project_id, "opt_fields=due_on,name,completed"
            )

            for i, item in enumerate(all_task):
                if (
                    (item["completed"] is False)
                    and (item["due_on"] is not None)
                    and (datetime.strptime(item["due_on"], "%Y-%m-%d").date() < target_date)
                ):
                    data = {
                        "name": item["name"],
                        "due_on": item["due_on"],
                    }
                    overdue_tasks.append(data)

            return overdue_tasks
        except Exception as e:
            raise


class GetSections(AsanaBase):
    def __init__(self, apikey):
        """親クラスの__init__を呼び出しを行う。

        Args:
            apikey (str): AsanaAPIのトークン
        """
        super().__init__(apikey)

    def sections_for_project(self, project_id):
        """プロジェクトからセクション一覧を返す。

        起点日は実行時の日付としている。

        Args:
            project_id (int): プロジェクトID

        Returns:
            list: セクションID一覧
        """
        try:
            if _check_project_id(project_id):
                url = self.aurl + f"/projects/{project_id}/sections/?opt_fields=name,gid"
                req = requests.get(url, auth=(self.apikey, ""))
                req.raise_for_status()
                data = req.json()

                return data["data"]
        except Exception as e:
            raise


class GetUsers(AsanaBase):
    def __init__(self, apikey):
        super().__init__(apikey)

    def all_users_for_workspace(self, workspace_id):
        """ワークスペースの全ユーザー情報を返す。

        Args:
            workspace_id (int): ワークスペースID

        Returns:
            list: 全ユーザー一覧
        """
        try:
            url = self.aurl + f"/workspaces/{workspace_id}/users/?opt_fields=name,gid"
            req = requests.get(url, auth=(self.apikey, ""))
            req.raise_for_status()
            data = req.json()

            return data["data"]
        except Exception as e:
            raise

    def target_user_for_workspace(self, workspace_id, target_username):
        """ワークスペースの対象ユーザーの情報を返す。

        Args:
            workspace_id (int): ワークスペースID
            target_username (str): 対象ユーザーの名前

        Returns:
            list: 対象ユーザー
        """
        try:
            url = self.aurl + f"/workspaces/{workspace_id}/users/?opt_fields=name,gid"
            req = requests.get(url, auth=(self.apikey, ""))
            req.raise_for_status()
            data = req.json()
            json_data = []

            for i, item in enumerate(data["data"]):
                if item["name"] == target_username:
                    json_data.append(item)
                    return json_data
            else:
                return "Target username does not exist"
        except Exception as e:
            raise


class GetCount(GetTasks):
    def __init__(self, apikey):
        """親クラスの__init__を呼び出しを行う。

        Args:
            apikey (str): AsanaAPIのトークン
        """
        super().__init__(apikey)

    def completed_tasks_for_project(self, project_id):
        """プロジェクトから完了タスク数を返す。

        Args:
            project_id ([int]): プロジェクトID

        Returns:
            int: 完了タスク数
        """
        try:
            all_task = super().tasks_for_project(project_id, "opt_fields=completed")
            completed_tasks_count = 0

            for i, item in enumerate(all_task):
                if item["completed"]:
                    completed_tasks_count += 1

            return completed_tasks_count
        except Exception as e:
            raise

    def uncompleted_tasks_for_project(self, project_id):
        """プロジェクトから未完了タスク数を返す。

        Args:
            project_id ([int]): プロジェクトID

        Returns:
            int: 未完了タスク数
        """
        try:
            all_task = super().tasks_for_project(project_id, "opt_fields=completed")
            uncompleted_tasks_count = 0

            for i, item in enumerate(all_task):
                if not item["completed"]:
                    uncompleted_tasks_count += 1

            return uncompleted_tasks_count
        except Exception as e:
            raise
