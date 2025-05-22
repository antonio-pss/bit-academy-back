from rest_framework import serializers

from bit_notes.models import Note, NoteContent


class NoteSerializer(serializers.ModelSerializer):
    notes = serializers.HyperlinkedRelatedField(
        many = True,
        required = False,
        view_name = 'note-detail',
        queryset = NoteContent.objects.all(),
    )

    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    expandable_fields = {
        'notes': (
            'bit_notes.serializers.NoteSerializer',
            {'many': True, 'fields': ('id', 'title', 'content', 'created_at')}
        ),
        'id_user': (
            'core.serializers.UserSerializer',
            {'many': False, 'fields': ('id', 'name', 'email')}
        ),
    }


class NoteContentSerializer(serializers.ModelSerializer):

    class Meta:
        model = NoteContent
        fields = '__all__'

    expandable_fields = {
        'id_note': (
            'bit_notes.serializers.NoteSerializer',
            {'many': False, 'fields': ('id', 'title', 'content', 'created_at')}
        ),
        'id_user': (
            'core.serializers.UserSerializer',
            {'many': False, 'fields': ('id', 'name', 'email')}
        ),
    }