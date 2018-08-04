# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class CoursesTeacher(models.Model):
    courses_id = models.IntegerField()
    teacher_id = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'courses_teacher'


class School(models.Model):
    id = models.IntegerField(primary_key=True)
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
    academy = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, db_column='academy')
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


class Tags(models.Model):
    tagid = models.AutoField(primary_key=True)
    tagname = models.CharField(max_length=100)
    pid = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'tags'


class Problem(models.Model):
    problem_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    input = models.TextField(blank=True, null=True)
    output = models.TextField(blank=True, null=True)
    sample_input = models.TextField(blank=True, null=True)
    sample_output = models.TextField(blank=True, null=True)
    spj = models.CharField(max_length=1)
    hint = models.TextField(blank=True, null=True)
    source = models.CharField(max_length=100, blank=True, null=True)
    in_date = models.DateTimeField(blank=True, null=True)
    time_limit = models.IntegerField()
    memory_limit = models.IntegerField()
    defunct = models.CharField(max_length=1)
    accepted = models.IntegerField(blank=True, null=True)
    submit = models.IntegerField(blank=True, null=True)
    solved = models.IntegerField(blank=True, null=True)
    problem_type = models.IntegerField()
    hastestdata = models.IntegerField(blank=True, null=True)
    owner = models.IntegerField(blank=True, null=True, default=-1)
    is_verify = models.IntegerField(blank=True, null=True, default=1)
    analysis = models.CharField(max_length=200, blank=True, null=True)
    difficulty = models.IntegerField(blank=True, null=True)
    tags = models.ManyToManyField(Tags, through='ProblemTag')

    class Meta:
        managed = True
        db_table = 'problem'


class ProblemTag(models.Model):
    problem_id = models.ForeignKey(Problem, on_delete=models.CASCADE, db_column='problem_id')
    tagid = models.ForeignKey(Tags, on_delete=models.CASCADE, db_column='tagid')

    class Meta:
        managed = True
        db_table = 'problem_tag'


class Solution(models.Model):
    problem_id = models.PositiveSmallIntegerField()
    solution_id = models.AutoField(primary_key=True)
    uid = models.PositiveSmallIntegerField(blank=True, null=True)
    user_id = models.CharField(max_length=48)
    time = models.PositiveSmallIntegerField()
    memory = models.PositiveSmallIntegerField()
    in_date = models.DateTimeField()
    result = models.IntegerField()
    language = models.PositiveIntegerField()
    ip = models.CharField(max_length=15)
    contest_id = models.PositiveSmallIntegerField(blank=True, null=True)
    valid = models.IntegerField()
    num = models.IntegerField()
    code_length = models.PositiveSmallIntegerField()
    judgetime = models.DateTimeField(blank=True, null=True)
    pass_rate = models.DecimalField(max_digits=2, decimal_places=2)
    lint_error = models.PositiveIntegerField()
    judger = models.CharField(max_length=16)
    problem_belong = models.PositiveIntegerField()
    exam_id = models.PositiveSmallIntegerField()
    test_id = models.PositiveIntegerField()
    protype = models.PositiveIntegerField(blank=True, null=True)
    fortest = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'solution'


class SourceCode(models.Model):
    solution_id = models.IntegerField(primary_key=True)
    source = models.TextField()

    class Meta:
        managed = True
        db_table = 'source_code'


class Runtimeinfo(models.Model):
    solution_id = models.IntegerField(primary_key=True)
    error = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'runtimeinfo'


class News(models.Model):
    news_id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='uid')
    title = models.CharField(max_length=200)
    content = models.TextField()
    time = models.DateTimeField()
    importance = models.IntegerField()
    defunct = models.CharField(max_length=1)

    class Meta:
        managed = True
        db_table = 'news'