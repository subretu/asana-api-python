from src.asana import asana


class TestGetSections:
    def test_sections_for_project(self, asanabase):
        asana_api = asana.GetSections(asanabase[0])
        result_data = asana_api.sections_for_project(asanabase[1])

        test_data = [
            {"gid": "2345678901234567", "name": "ToDo"},
            {"gid": "2345678901234568", "name": "処理中"},
            {"gid": "2345678901234569", "name": "完了"},
        ]

        assert result_data == test_data
