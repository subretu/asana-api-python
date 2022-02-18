from src.asana import asana


class TestGetCount:
    def test_completed_tasks_for_project(self, asanabase):
        asana_api = asana.GetCount(asanabase[0])
        result_data = asana_api.completed_tasks_for_project(asanabase[1])

        assert result_data == 2

    def test_uncompleted_tasks_for_project(self, asanabase):
        asana_api = asana.GetCount(asanabase[0])
        result_data = asana_api.uncompleted_tasks_for_project(asanabase[1])

        assert result_data == 1
