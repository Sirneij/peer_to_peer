from typing import Any


class User:
    _user_data: list[dict[str, Any]] = []

    @property
    def user_data(self) -> list[dict[str, Any]]:
        return self._user_data

    def set_user_data(self, data):
        self._user_data = self._user_data.append(data)

    def return_user(self, username) -> dict[str, Any] | None:
        for d in self._user_data:
            if username in d.values():
                print("here!")
                return d
        return None
