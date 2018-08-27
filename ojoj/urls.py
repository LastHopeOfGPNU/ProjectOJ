from django.urls import path
from . import views
from .module.user import *
from .module.class_view import *
from .module.student import *
from .module.school import *
from .module.problem import *
from .module.news import *
from .module.feedback import *
from .module.maintenance import *
from .module.contest import *
from .module.article import *
from .module.tag import *
from .module.rank import *
from .module.state import *
from .module.about_us import *
from .module.quiz import *
from .module.course import *
from django.conf.urls import url

app_name = 'ojoj'
urlpatterns = [
    # API URL
    path('captcha', views.captcha, name='captcha'),
    url('users/login/$', UserLoginView.as_view()),
    url('users/register/$', UserRegisterView.as_view()),
    url('users$', UserView.as_view()),
    url('users/detail', UserDetailView.as_view()),
    url('users/uploadImage', UserUploadImageView.as_view()),
    url('users/teachers$', TeacherView.as_view()),
    url('users/teachers/upload', TeacherFileView.as_view()),
    url('classes$', ClassView.as_view()),
    url('classes/detail', ClassDetailView.as_view()),
    url('students$', StudentView.as_view()),
    url('students/upload', StudentFileView.as_view()),
    url('students/detail', StudentDetailView.as_view()),
    url('schools$', SchoolView.as_view()),
    url('^problems$', ProblemView.as_view()),
    url('problems/detail', ProblemDetailView.as_view()),
    url('problems/submit', ProblemSubmitView.as_view()),
    url('news$', NewsView.as_view()),
    url('feedbacks$', FeedbackView.as_view()),
    url('maintenance$', MaintenanceView.as_view()),
    url('contests$', ContestView.as_view()),
    url('contests/detail', ContestDetailView.as_view()),
    url('contests/rank', ContestRankView.as_view()),
    url('articles$', ArticleView.as_view()),
    url('articles/labels', LabelView.as_view()),
    url('articles/index', ArticleIndexView.as_view()),
    url('tags$', TagView.as_view()),
    url('ranks$', RankView.as_view()),
    url('rank_all', RankAllView.as_view()),
    url('states$', StateView.as_view()),
    url('about_us', AboutUsView.as_view()),
    url('quiz/templates', TemplateView.as_view()),
    url('quiz/problem', QuizProblemView.as_view()),
    url('quiz/detail', QuizDetailView.as_view()),
    url('quiz$', QuizView.as_view()),
    url('courses/exams/problems', ExamProblemView.as_view()),
    url('courses/exams', CourseExamView.as_view()),
    url('courses', CourseView.as_view()),
    # 页面URL
    path('', views.index, name='index'),
]