from src.asana import asana
import pytest


class TestGetTasks:
    def test_tasks_for_project(self, asanabase):
        asana_api = asana.GetTasks(asanabase[0])
        result_data = asana_api.tasks_for_project(asanabase[1], "opt_fields=name,gid")

        test_data = [
            {"gid": "1234567891234567", "name": "タスクXXXXX"},
            {"gid": "1234567891234568", "name": "タスクYYYYY"},
            {"gid": "1234567891234569", "name": "タスクZZZZZ"},
        ]

        assert result_data == test_data

    def test_overdue_tasks_for_project(self, asanabase):
        asana_api = asana.GetTasks(asanabase[0])
        result_data = asana_api.overdue_tasks_for_project(asanabase[1])

        test_data = [{"name": "タスクZZZZZ", "due_on": "2022-02-01"}]

        assert result_data == test_data

    def test_tasks_for_project_error(self, asanabase):
        with pytest.raises(Exception) as e:
            asana_api = asana.GetCount(asanabase[0])
            _ = asana_api.tasks_for_project(12345, "opt_fields=name,gid")

        assert str(e.value) == "invalid project_id"
