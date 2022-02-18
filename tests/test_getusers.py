from src.asana import asana


class TestGetUsers:
    def test_all_users_for_workspace(self, asanabase):
        asana_api = asana.GetUsers(asanabase[0])
        result_data = asana_api.all_users_for_workspace(asanabase[2])

        test_data = [
            {"gid": "3456789012345678", "name": "Taro Test"},
            {"gid": "3456789012345679", "name": "Jiro Test"}
        ]

        assert result_data == test_data

    def test_target_user_for_workspace(self, asanabase):
        asana_api = asana.GetUsers(asanabase[0])
        result_data = asana_api.target_user_for_workspace(asanabase[2], "Taro Test")

        test_data = [{"gid": "3456789012345678", "name": "Taro Test"}]

        assert result_data == test_data
