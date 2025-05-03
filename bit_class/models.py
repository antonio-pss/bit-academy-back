from django.db import models

from bit_school.models import CourseModuleDiscipline
from core.models import ModelBase, User


class Class(ModelBase):
    name = models.CharField(max_length=50, db_column="tx_name", )
    description = models.TextField(db_column="tx_description", )
    id_course_module_discipline = models.ForeignKey(CourseModuleDiscipline, db_column="fk_course_module_discipline", on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'class'


class ClassRole(ModelBase):
    name = models.CharField(max_length=50, db_column="tx_name", )

    class Meta:
        managed = True
        db_table = 'class_role'


class ClassMember(ModelBase):
    id_class_role = models.ForeignKey(ClassRole, db_column="fk_class_role", on_delete=models.CASCADE)
    id_class = models.ForeignKey(Class, db_column="fk_class", on_delete=models.CASCADE)
    id_user = models.ForeignKey(User, db_column="fk_user", on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'class_member'


class Frequency(ModelBase):
    id_class_member = models.ForeignKey(ClassMember, db_column="fk_class_member", on_delete=models.CASCADE)
    day = models.DateField(db_column="dt_day", )

    class Meta:
        managed = True
        db_table = 'frequency'


class Status(ModelBase):
    name = models.CharField(max_length=50, db_column="tx_name", )

    class Meta:
        managed = True
        db_table = 'status'


class Time(ModelBase):
    id_frequency = models.ForeignKey(Frequency, db_column="fk_frequency", on_delete=models.CASCADE)
    id_status = models.ForeignKey(Status, db_column="fk_status", on_delete=models.CASCADE)
    start_hour = models.DateTimeField(db_column="dt_start_hour", )
    end_hour = models.DateTimeField(db_column="dt_end_hour", )

    class Meta:
        managed = True
        db_table = 'time'


class Activity(ModelBase):
    title = models.CharField(max_length=50, db_column="tx_title", )
    description = models.TextField(db_column="tx_description", )
    limit_date = models.DateField(db_column="dt_limit_date", )

    class Meta:
        managed = True
        db_table = 'activity'


class Grade(ModelBase):
    score = models.IntegerField(db_column="nb_score", )
    id_class_member = models.ForeignKey(ClassMember, db_column="fk_class_member", on_delete=models.CASCADE)
    id_activity = models.ForeignKey(Activity, db_column="fk_activity", on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'grade'


class TaskSubmission(ModelBase):
    id_activity = models.ForeignKey(Activity, db_column="fk_activity", on_delete=models.CASCADE)
    text_response = models.TextField(db_column="tx_text_response")
    file_upload = models.TextField(db_column="tx_file_upload", )
    graded = models.BooleanField(db_column="cs_graded", )

    class Meta:
        managed = True
        db_table = 'task_submission'
