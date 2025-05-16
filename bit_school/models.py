from django.db import models

from core.models import ModelBase, User


class InstitutionRole(ModelBase):
    name = models.CharField(max_length=50, db_column="tx_name")

    class Meta:
        managed = True
        db_table = 'institution_role'


class Institution(ModelBase):
    name = models.CharField(
        max_length=50,
        db_column="tx_name",
        default='without_institutional_link'
    )

    class Meta:
        managed = True
        db_table = 'institution'


class UserInstitutionRole(ModelBase):
    id_user = models.ForeignKey(User, db_column="fk_user", on_delete=models.CASCADE)
    id_institution = models.ForeignKey(
        Institution,
        db_column="fk_institution",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    id_institution_role = models.ForeignKey(
        InstitutionRole,
        db_column="fk_institution_role",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        managed = True
        db_table = 'user_institution_role'


class Course(ModelBase):
    name = models.CharField(max_length=50, db_column="tx_name",)
    description = models.TextField(db_column="tx_description", )
    id_institution = models.ForeignKey(Institution, db_column="fk_institution", on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'course'


class Module(ModelBase):
    name = models.CharField(max_length=50, db_column="tx_name", default='default')

    class Meta:
        managed = True
        db_table = 'module'


class Discipline(ModelBase):
    name = models.CharField(max_length=50, db_column="tx_name", )
    description = models.TextField(db_column="tx_description", )
    workload = models.IntegerField(db_column="nb_workload", )

    class Meta:
        managed = True
        db_table = 'discipline'


class CourseModuleDiscipline(ModelBase):
    id_course = models.ForeignKey(Course, db_column="fk_course", on_delete=models.CASCADE)
    id_module = models.ForeignKey(Module, db_column="fk_module", on_delete=models.CASCADE)
    id_discipline = models.ForeignKey(Discipline, db_column="fk_discipline", on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'course_module_discipline'
