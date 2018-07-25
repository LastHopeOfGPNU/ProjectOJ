# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class School(models.Model):
    name = models.CharField(max_length=32, blank=True, null=True)
    school_id = models.IntegerField(blank=True, null=True)
    academy_id = models.IntegerField(blank=True, null=True)
    remark = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'school'


class Courses(models.Model):
    courses_id = models.AutoField(primary_key=True)
    courses_name = models.CharField(max_length=100, blank=True, null=True)
    grade = models.IntegerField()
    term = models.IntegerField()
    open = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'courses'


class Class(models.Model):
    class_id = models.CharField(primary_key=True, max_length=11)
    class_name = models.CharField(max_length=100, blank=True, null=True)
    grade = models.IntegerField(blank=True, null=True)
    academy_id = models.ForeignKey(School, on_delete=models.CASCADE, db_column='academy_id')
    studentnum = models.IntegerField(blank=True, null=True)
    courses = models.ManyToManyField(Courses, through='CoursesClass')

    class Meta:
        managed = True
        db_table = 'class'


class CoursesClass(models.Model):
    courses_id = models.ForeignKey(Courses, on_delete=models.CASCADE, db_column='courses_id')
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE, db_column='class_id')

    class Meta:
        managed = True
        db_table = 'courses_class'


class Users(models.Model):
    uid = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=48)
    email = models.CharField(max_length=100, blank=True, null=True)
    submit = models.IntegerField(blank=True, null=True)
    solved = models.IntegerField(blank=True, null=True)
    defunct = models.CharField(max_length=1)
    ip = models.CharField(max_length=20)
    accesstime = models.DateTimeField(blank=True, null=True)
    volume = models.IntegerField(default=1)
    language = models.IntegerField(default=1)
    password = models.CharField(max_length=32, blank=True, null=True)
    reg_time = models.DateTimeField(blank=True, null=True)
    nick = models.CharField(max_length=100)
    signature = models.TextField(blank=True, null=True)
    school = models.CharField(max_length=100)
    identity = models.CharField(max_length=1)
    birthday = models.DateTimeField(blank=True, null=True)
    sex = models.IntegerField(blank=True, null=True)
    qq = models.CharField(max_length=20, blank=True, null=True)
    academy = models.IntegerField(blank=True, null=True)
    major = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    contact = models.CharField(max_length=255, blank=True, null=True)
    cookie = models.CharField(max_length=32, blank=True, null=True)
    login_time = models.DateTimeField(blank=True, null=True)
    code = models.CharField(max_length=20, blank=True, null=True)
    class_id = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, db_column='class_id')
    grade = models.IntegerField(blank=True, null=True)
    avatarurl = models.CharField(db_column='avatarUrl', max_length=500, blank=True, null=True)  # Field name made lowercase.
    last_submit = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'users'


class Loginlog(models.Model):
    id = models.BigAutoField(primary_key=True)
    captcha = models.TextField()
    ip = models.CharField(max_length=100)
    time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'loginlog'

