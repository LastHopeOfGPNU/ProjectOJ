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
    open = models.IntegerField(default=1)

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
    submit = models.IntegerField(blank=True, null=True, default=0)
    solved = models.IntegerField(blank=True, null=True, default=0)
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
    spj = models.CharField(max_length=1, default="")
    hint = models.TextField(blank=True, null=True)
    source = models.CharField(max_length=100, blank=True, null=True)
    in_date = models.DateTimeField(blank=True, null=True)
    time_limit = models.IntegerField(default=0)
    memory_limit = models.IntegerField(default=0)
    defunct = models.CharField(max_length=1, default='N')
    accepted = models.IntegerField(blank=True, null=True, default=0)
    submit = models.IntegerField(blank=True, null=True, default=0)
    solved = models.IntegerField(blank=True, null=True)
    problem_type = models.IntegerField()
    hastestdata = models.IntegerField(blank=True, null=True)
    owner = models.IntegerField(blank=True, null=True, default=-1)
    is_verify = models.IntegerField(blank=True, null=True, default=1)
    analysis = models.CharField(max_length=200, blank=True, null=True)
    difficulty = models.IntegerField(blank=True, null=True)
    accept_rate = models.FloatField(default=0)
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
    time = models.PositiveSmallIntegerField(default=0)
    memory = models.PositiveSmallIntegerField(default=0)
    in_date = models.DateTimeField()
    result = models.IntegerField(default=0)
    language = models.PositiveIntegerField()
    ip = models.CharField(max_length=15)
    contest_id = models.PositiveSmallIntegerField(blank=True, null=True)
    valid = models.IntegerField(default=1)
    num = models.IntegerField(default=-1)
    code_length = models.PositiveSmallIntegerField()
    judgetime = models.DateTimeField(blank=True, null=True)
    pass_rate = models.DecimalField(max_digits=2, decimal_places=2, default=0.00)
    lint_error = models.PositiveIntegerField(default=0)
    judger = models.CharField(max_length=16, default='LOCAL')
    problem_belong = models.PositiveIntegerField(default=0)
    exam_id = models.PositiveSmallIntegerField(default=0)
    test_id = models.PositiveIntegerField(default=0)
    protype = models.PositiveIntegerField(blank=True, null=True)
    fortest = models.CharField(max_length=45, blank=True, null=True, default=None)

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


class Feedback(models.Model):
    fid = models.AutoField(primary_key=True)
    uid = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='uid')
    type = models.IntegerField(blank=True, null=True)
    is_mark = models.IntegerField(blank=True, null=True, default=0)
    is_solved = models.IntegerField(blank=True, null=True, default=0)
    title = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    remark = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'feedback'

class Maintenance(models.Model):
    id = models.AutoField(primary_key=True)
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'maintenance'


class Contest(models.Model):
    contest_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    begin = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    state = models.CharField(max_length=1, default='N')
    holder = models.IntegerField(blank=True, null=True)
    type = models.IntegerField()
    password = models.CharField(max_length=16)
    score = models.IntegerField(blank=True, null=True)
    problem_set = models.ManyToManyField(Problem, through='ContestProblem')

    class Meta:
        managed = True
        db_table = 'contest'


class ContestProblem(models.Model):
    problem_id = models.ForeignKey(Problem, on_delete=models.CASCADE, db_column='problem_id')
    contest_id = models.ForeignKey(Contest, on_delete=models.CASCADE, db_column='contest_id')
    rank = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'contest_problem'


class Article(models.Model):
    articleid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    publisher = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='publisherid')
    content = models.TextField(blank=True, null=True)
    publishtime = models.DateTimeField(blank=True, null=True)
    pvnum = models.IntegerField(blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    agreenum = models.IntegerField()
    commentnum = models.IntegerField()
    summary = models.CharField(max_length=500, blank=True, null=True)
    isMarkdown = models.IntegerField(db_column='isMarkdown', blank=True, null=True)
    mcontent = models.TextField(blank=True, null=True)
    tagnames = models.CharField(max_length=255, blank=True, null=True)
    labelid = models.IntegerField(blank=True, null=True)
    isTop = models.IntegerField(db_column='isTop', blank=True, null=True)
    isQuality = models.IntegerField(db_column='isQuality', blank=True, null=True)
    isAuthorized = models.IntegerField(db_column='isAuthorized', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'article'


# 文章的标签
class Label(models.Model):
    labelid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    pid = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=188, blank=True, null=True)
    type = models.CharField(max_length=45, blank=True, null=True)
    iconUrl = models.CharField(db_column='iconUrl', max_length=1000, blank=True, null=True)
    bannerUrl = models.CharField(db_column='bannerUrl', max_length=1000, blank=True, null=True)
    articles = models.ManyToManyField(Article, through='ArticleLabel')

    class Meta:
        managed = True
        db_table = 'label'


class ArticleLabel(models.Model):
    articleid = models.ForeignKey(Article, on_delete=models.CASCADE, db_column='articleid')
    labelid = models.ForeignKey(Label, on_delete=models.CASCADE, db_column='labelid')

    class Meta:
        managed = True
        db_table = 'article_label'


class AboutUs(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    avatarurl = models.CharField(db_column='avatarUrl', max_length=500, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    job = models.CharField(max_length=255, blank=True, null=True)
    grade = models.IntegerField(default=0)

    class Meta:
        managed = True
        db_table = 'about_us'


class Template(models.Model):
    template_id = models.AutoField(primary_key=True)
    uid = models.IntegerField()
    name = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'template'


class QuestionType(models.Model):
    question_type_id = models.AutoField(primary_key=True)
    problem_type = models.IntegerField()
    question_num = models.IntegerField()
    type_bonus = models.FloatField()
    template = models.ForeignKey(Template, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'question_type'


class CoursesQuiz(models.Model):
    quiz_id = models.AutoField(primary_key=True)
    quiz_name = models.CharField(max_length=255, blank=True, null=True)
    quiz_manual = models.IntegerField(default=1)
    course_id = models.IntegerField()
    quiz_state = models.IntegerField(default=0)
    quiz_date = models.DateTimeField()
    quiz_duration = models.IntegerField()
    template = models.ForeignKey('Template', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'courses_quiz'


class CoursesQuizProblem(models.Model):
    quiz_id = models.ForeignKey(CoursesQuiz, on_delete=models.CASCADE, db_column='quiz_id')
    problem_id = models.IntegerField()
    item_id = models.IntegerField()
    problem_type = models.IntegerField()
    problem_bonus = models.FloatField()

    class Meta:
        managed = True
        db_table = 'courses_quiz_problem'


class ContestFinish(models.Model):
    contest_finish_id = models.AutoField(primary_key=True)
    contest_id = models.PositiveSmallIntegerField()
    uid = models.PositiveSmallIntegerField()
    finish = models.CharField(max_length=30)
    submit = models.CharField(max_length=30)
    all_time = models.PositiveIntegerField()
    accept_num = models.PositiveSmallIntegerField()
    submit_num = models.PositiveSmallIntegerField()

    class Meta:
        managed = True
        db_table = 'contest_finish'


class CoursesExam(models.Model):
    exam_id = models.AutoField(primary_key=True)
    exam_name = models.CharField(max_length=100, blank=True, null=True)
    create_time = models.DateTimeField()
    stop_time = models.DateTimeField()
    courses_id = models.ForeignKey(Courses, on_delete=models.CASCADE, db_column='courses_id')
    uid = models.IntegerField()
    all_num = models.IntegerField()
    solve_num = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'courses_exam'


class CoursesExamProblem(models.Model):
    problem_id = models.IntegerField(blank=True, null=True)
    exam_id = models.IntegerField(blank=True, null=True)
    totolscore = models.IntegerField(blank=True, null=True)
    accept_num = models.IntegerField()
    submit_num = models.IntegerField()
    rank = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'courses_exam_problem'


class QuizDetail(models.Model):
    uid = models.IntegerField()
    quiz_id = models.IntegerField()
    item_id = models.IntegerField()
    problem_id = models.IntegerField()
    user_answer = models.TextField()
    score = models.IntegerField(default=0)

    class Meta:
        managed = True
        db_table = 'quiz_detail'