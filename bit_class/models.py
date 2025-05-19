from django.db import models

from bit_school.models import CourseModuleDiscipline
from core.models import ModelBase, User


class Class(ModelBase, models.Model):
    name = models.CharField(max_length=50, db_column="tx_name", )
    description = models.TextField(db_column="tx_description", )
    id_course_module_discipline = models.ForeignKey(
        CourseModuleDiscipline,
        db_column="fk_course_module_discipline",
        on_delete=models.CASCADE,
        default=1, #ID sem vinculo institucional
    )

    class Meta:
        managed = True
        db_table = 'class'


class ClassRole(ModelBase, models.Model):
    ROLE_CHOICES = (
        ('TCHR', 'Teacher'),
        ('STD', 'Student'),
        ('PRIN', 'Principal'),
        ('TRN', 'Trainee')
    )
    role = models.CharField(
        null=False,
        max_length=4,
        choices=ROLE_CHOICES,
        db_column="tx_role",
        unique=True,
        default='STD',
    )

    class Meta:
        managed = True
        ordering = ['role']
        db_table = 'class_role'


class ClassMember(ModelBase, models.Model):
    id_class_role = models.ForeignKey(ClassRole, db_column="fk_class_role", on_delete=models.CASCADE)
    id_class = models.ForeignKey(Class, db_column="fk_class", on_delete=models.CASCADE)
    id_user = models.ForeignKey(User, db_column="fk_user", on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'class_member'


class Frequency(ModelBase, models.Model):
    id_class_member = models.ForeignKey(ClassMember, db_column="fk_class_member", on_delete=models.CASCADE)
    day = models.DateField(db_column="dt_day", )

    class Meta:
        managed = True
        db_table = 'frequency'


class Status(ModelBase, models.Model):
    name = models.CharField(max_length=50, db_column="tx_name", )

    class Meta:
        managed = True
        db_table = 'status'


class Time(ModelBase, models.Model):
    id_frequency = models.ForeignKey(Frequency, db_column="fk_frequency", on_delete=models.CASCADE)
    id_status = models.ForeignKey(Status, db_column="fk_status", on_delete=models.CASCADE)
    start_hour = models.DateTimeField(db_column="dt_start_hour", )
    end_hour = models.DateTimeField(db_column="dt_end_hour", )

    class Meta:
        managed = True
        db_table = 'time'


class Activity(ModelBase, models.Model):
    title = models.CharField(max_length=50, db_column="tx_title", )
    description = models.TextField(db_column="tx_description", )
    limit_date = models.DateField(db_column="dt_limit_date", )

    class Meta:
        managed = True
        db_table = 'activity'


class TaskSubmission(ModelBase, models.Model):
    id_activity = models.ForeignKey(
        Activity,
        db_column="fk_activity",
        on_delete=models.CASCADE
    )
    id_user = models.ForeignKey(
        User,
        db_column="fk_user",
        on_delete=models.CASCADE,
    )
    text_response = models.TextField(
        db_column="tx_text_response",
        blank=False,
        null=True,
    )
    file_upload = models.URLField(
        db_column="tx_file_upload",
        blank=True,
        null=True,
    )
    delivered = models.BooleanField(
        db_column="cs_graded",
        default=False,
    )

    class Meta:
        managed = True
        db_table = 'task_submission'


class Grade(ModelBase, models.Model):
    score = models.IntegerField(
        db_column="nb_score",
        blank=False,
        null=False,
        default=0
    )
    id_task_submission = models.ForeignKey(
        TaskSubmission,
        db_column="fk_task_submission",
        on_delete=models.CASCADE,
        default=1 #temporário
    )

    class Meta:
        managed = True
        db_table = 'grade'


class ClassInvitation(ModelBase, models.Model):
    email = models.EmailField(db_column='tx_email')
    id_class = models.ForeignKey(
        'Class',
        db_column='fk_class',
        on_delete=models.CASCADE,
        related_name='invitations'
    )
    id_class_role = models.ForeignKey(
        'ClassRole',
        db_column='fk_role',
        on_delete=models.CASCADE
    )
    is_accepted = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'class_invitation'
