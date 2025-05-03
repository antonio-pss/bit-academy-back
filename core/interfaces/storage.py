from typing import BinaryIO


class StorageInterface:
    def store_avatar(self, avatar: BinaryIO, user_id: int) -> str:
        pass

    def get_avatar_url(self, avatar_path: str) -> str:
        pass

    def store_file_for_class(self, file: BinaryIO, filename: str, class_id: int) -> str:
        pass

    def get_file_url(self, file_path: str) -> str:
        pass