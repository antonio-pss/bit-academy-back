from django.db import models

from core.models import ModelBase, User


class Note(ModelBase):
    id_user = models.ForeignKey(User, db_column="fk_user", on_delete=models.CASCADE)
    title = models.CharField(max_length=100, db_column="tx_title", )
    content = models.TextField(db_column="tx_content", )

    class Meta:
        managed = True
        db_table = 'note'


class FlashCard(ModelBase):
    id_user = models.ForeignKey(User, db_column="fk_user", on_delete=models.CASCADE)
    question = models.CharField(max_length=200, db_column="tx_question")
    answer = models.CharField(max_length=200, db_column="tx_answer")

    class Meta:
        managed = True
        db_table = 'flashcard'
