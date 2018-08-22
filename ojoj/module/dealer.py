from django.utils import timezone
from ..models import Problem

class ProblemDealer:

    def edit(self, params, problem_type):
        problem = None
        if problem_type == 1:
            problem = self.edit_type_fill(params)
        elif problem_type == 2:
            problem = self.edit_type_choice(params)
        elif problem_type == 3:
            problem = self.edit_type_code(params)
        elif problem_type == 4:
            problem = self.edit_type_ask(params)
        elif problem_type == 5:
            problem = self.edit_type_tf(params)
        return problem

    def create(self, params, problem_type):
        problem = None
        if problem_type == 1:
            problem = self.add_type_fill(params)
        elif problem_type == 2:
            problem = self.add_type_choice(params)
        elif problem_type == 3:
            problem = self.add_type_code(params)
        elif problem_type == 4:
            problem = self.add_type_ask(params)
        elif problem_type == 5:
            problem = self.add_type_tf(params)
        return problem

    def edit_type_fill(self, params):
        problem = Problem.objects.get(problem_id=params.pop('problem_id'))
        now = timezone.now()
        problem.title = params['title']
        problem.description = params['description']
        problem.hint = params['hint']
        problem.sample_output = params['sample_output']
        problem.in_date = now
        return problem

    def edit_type_choice(self, params):
        problem = Problem.objects.get(problem_id=params.pop('problem_id'))
        now = timezone.now()
        problem.title = params['title']
        problem.description = params['description']
        problem.in_date = now
        problem.sample_input = params['sample_input']
        problem.sample_output = params['sample_output']
        return problem

    def edit_type_code(self, params):
        problem = Problem.objects.get(problem_id=params.pop('problem_id'))
        params['in_date'] = timezone.now()
        for key, value in params.items():
            setattr(problem, key, value)
        return problem

    def edit_type_ask(self, params):
        problem = Problem.objects.get(problem_id=params.pop('problem_id'))
        now = timezone.now()
        problem.title = params['title']
        problem.description = params['description']
        problem.in_date = now
        return problem

    def edit_type_tf(self, params):
        problem = Problem.objects.get(problem_id=params.pop('problem_id'))
        now = timezone.now()
        problem.title = params['title']
        problem.description = params['description']
        problem.in_date = now
        problem.sample_output = params['sample_output']
        return problem

    def add_type_fill(self, params):
        # 添加1类题目（填空题）
        now = timezone.now()
        problem = Problem.objects.create(hint=params['hint'], title=params['title'], description=params['description'],
                                         sample_output=params['sample_output'], in_date=now, problem_type=1)
        return problem

    def add_type_choice(self, params):
        # 添加2类题目（选择题）
        now = timezone.now()
        problem = Problem.objects.create(title=params['title'], description=params['description'],
                                         sample_input=params['sample_input'], sample_output=params['sample_output'],
                                         in_date=now, problem_type=2)
        return problem

    def add_type_code(self, params):
        # 添加3类题目（编程题）
        params['in_date'] = timezone.now()
        problem = Problem.objects.create(**params)
        return problem

    def add_type_ask(self, params):
        # 添加4类题目（问答题）
        now = timezone.now()
        problem = Problem.objects.create(title=params['title'], description=params['description'],
                                         in_date=now, problem_type=4)
        return problem

    def add_type_tf(self, params):
        # 添加5类题目（判断题）
        now = timezone.now()
        problem = Problem.objects.create(title=params['title'], description=params['description'],
                                         sample_output=params['sample_output'],
                                         in_date=now, problem_type=5)
        return problem
