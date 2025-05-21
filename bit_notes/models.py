from django.db import models

from core.models import ModelBase, User


class Note(ModelBase):
    id_user = models.ForeignKey(User, db_column="fk_user", on_delete=models.CASCADE)
    notes = models.ManyToManyField(
        to='core.models.User',
        through='NoteContent',
    )

    class Meta:
        managed = True
        db_table = 'note'


class NoteContent(ModelBase):
    title = models.CharField(max_length=50, db_column="tx_title")
    content = models.TextField(db_column="tx_content")
    id_note = models.ForeignKey(Note, db_column="fk_note", on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'note_content'


class FlashCard(ModelBase):
    id_user = models.ForeignKey(User, db_column="fk_user", on_delete=models.CASCADE)
    question = models.CharField(max_length=200, db_column="tx_question")
    answer = models.CharField(max_length=200, db_column="tx_answer")

    class Meta:
        managed = True
        db_table = 'flashcard'
