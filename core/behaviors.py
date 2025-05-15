from rest_framework.response import Response

from core.factories import get_storage_service

class MinionStorageBehavior:

    def upload_user_avatar(user, avatar_file):
        storage = get_storage_service()
        avatar_path = storage.store_avatar(avatar_file, user.id)
        avatar_url = storage.get_avatar_url(avatar_path)
        user.avatar = avatar_path
        user.save(update_fields=['avatar'])
        return avatar_url

    def upload_class_file(file, filename, class_id):
        storage = get_storage_service()
        file_path = storage.store_class_file(file, filename, class_id)
        return storage.get_file_url(file_path)

    def handle_upload_avatar(user, avatar):
        avatar_url = upload_user_avatar(user, avatar)
        return Response({'avatar_url': avatar_url})

    def handle_upload_class_file(class_id, file, filename):
        file_url = upload_class_file(file, filename, class_id)
        return Response({'file_url': file_url})

