from rest_framework import generics
from rest_framework.response import Response
from django.utils import timezone
from .core import BaseListView
from .dealer import ProblemDealer
from ..utils import data_wrapper, get_params_from_post
from ..models import Problem, Solution, Users, ProblemTag, Tags, SourceCode
from ..serializers import ProblemSerializer, SolutionSerializer, ProblemDetailSerializer, ProblemTypeSerializer
import json


# 获取用户的做题情况
# 已完成列表：[{题号: a, 通过数：b, 提交数：}, ...]
# 未完成列表：[{题号: a, 通过数：0, 提交数：}, ...]
def get_problem_info(uid):
    done_list = []
    not_done_list = []
    # 所有已做题目
    all = Solution.objects.filter(uid=uid).order_by('problem_id')
    # 已通过题目
    done = all.filter(result=4)
    for problem in done.values('problem_id').distinct():
        problem_id = problem['problem_id']
        total = Solution.objects.filter(uid=uid, problem_id=problem_id)
        done_list.append({
            'problem_id': problem_id,
            'submit': total.count(),
            'accepted': total.filter(result=4).count()
        })
    # 未通过列表
    not_done = all.exclude(problem_id__in=done.values_list('problem_id', flat=True))
    for problem in not_done.values('problem_id').distinct():
        problem_id = problem['problem_id']
        total = Solution.objects.filter(uid=uid, problem_id=problem_id)
        not_done_list.append({
            'problem_id': problem_id,
            'submit': total.count(),
            'accepted': total.filter(result=4).count()
        })
    return {
        'done_list': done_list,
        'not_done_list': not_done_list
    }


class ProblemSubmitView(generics.GenericAPIView):

    # 获取判题结果
    def get(self, request):
        try:
            problem_id = request.GET['problem_id']
            uid = request.GET['uid']
            solution = Solution.objects.filter(uid=uid, problem_id=problem_id).order_by('-solution_id')
            if solution.exists():
                solution = solution[0]
            else:
                solution = None
            data = SolutionSerializer(solution).data
        except:
            return Response(data_wrapper(msg=20001, success="false"))
        return Response(data_wrapper(data=data, success="true"))

    # 提交代码
    def post(self, request):
        namedict = {'uid': 20001, 'problem_id': 20001, 'protype': 20001, 'source': 20001, 'language': 20001}
        params = get_params_from_post(request, namedict)
        if params.pop('error'):
            return Response(data_wrapper(msg=20001, success="false"))
        try:
            user = Users.objects.get(uid=params['uid'])
            source = params.pop('source')
            params['user_id'] = user.user_id
            params['ip'] = request.META['REMOTE_ADDR']
            params['in_date'] = timezone.now()
            params['code_length'] = len(source)
            # 做solution表
            solution = Solution.objects.create(**params)
            solution.save()
            # 做source_code表
            source_code = SourceCode.objects.create(solution_id=solution.solution_id,
                                                    source=source)
            source_code.save()
            # 更新用户提交时间
            user.last_submit = params['in_date']
            user.save()
        except:
            return Response(data_wrapper(msg=20001, success="false"))
        return Response(data_wrapper(success="true"))


class ProblemView(BaseListView):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer

    def delete(self, request):
        try:
            problem_id = request.GET['problem_id']
            problem = self.get_queryset().get(problem_id=problem_id)
            # 删除问题
            problem.delete()
            # 删除问题相关solution
            solutions = Solution.objects.filter(problem_id=problem_id)
            solutions.delete()
            # TODO: 删除相关数据文件
        except:
            return Response(data_wrapper(success="false", msg=20001))
        return Response(data_wrapper(success="true"))

    def get_dataset(self, request):
        title = request.GET.get('title', None)
        problem_id = request.GET.get('problem_id', None)
        problem_type = request.GET.get('problem_type', None)
        tagid = request.GET.get('tagid', None)
        defunct = request.GET.get('defunct', None)
        accept_rate = request.GET.get('accept_rate', None)
        sort = request.GET.get('sort', None)
        finished_by = request.GET.get('finished_by', None)
        dataset = self.get_queryset().order_by('problem_id')

        if tagid:
            dataset = dataset.filter(tags__tagid=tagid)
        if title:
            dataset = dataset.filter(title__contains=title)
        if problem_id:
            dataset = dataset.filter(problem_id=problem_id)
        if problem_type:
            dataset = dataset.filter(problem_type=problem_type)
        if defunct:
            dataset = dataset.filter(defunct=defunct)
        if sort:
            if sort.lower() == 'desc':
                dataset = dataset.order_by('-accept_rate')
                # dataset = dataset.extra(select={'rate': 'accepted/submit'}).order_by('-rate')
            elif sort.lower() == 'asc':
                dataset = dataset.order_by('accept_rate')
                # dataset = dataset.extra(select={'rate': 'accepted/submit'}).order_by('rate')
        if accept_rate:
            if accept_rate == '1':
                rate_range = (0.8, 1)
            elif accept_rate == '2':
                rate_range = (0.6, 0.8)
            elif accept_rate == '3':
                rate_range = (0.4, 0.6)
            else:
                rate_range = (0, 0.4)
            dataset = dataset.filter(accept_rate__range=rate_range)
        if finished_by:
            solution = Solution.objects.filter(uid=finished_by)
            dataset = dataset.filter(problem_id__in=solution.values_list('problem_id', flat=True))

        return dataset.filter(is_verify=1)


class ProblemDetailView(generics.GenericAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemTypeSerializer  # ProblemDetailSerializer
    dealer = ProblemDealer()

    def get(self, request):
        try:
            uid = request.GET.get('uid', None)
            problem_id = request.GET['problem_id']

            problem = self.get_queryset().get(problem_id=problem_id)
            prob_ser = self.get_serializer(problem)
            data = prob_ser.data
            if uid:
                user = Users.objects.get(uid=uid)
                # 取最新的solution
                solution = Solution.objects.filter(uid=user.uid, problem_id=problem_id).order_by('-solution_id')
                if solution.exists():
                    solution = solution[0]
                    solu_ser = SolutionSerializer(solution)
                    solu_data = solu_ser.data
                    if problem.problem_type == 1 or problem.problem_type == 2 or problem.problem_type == 4 or problem.problem_type == 5:
                        solu_data.update({'sample_output': problem.sample_output})
                    data.update(solu_data)
                elif user.identity == '3':
                    data.update({'hint': problem.hint, 'sample_output': problem.sample_output})
            return Response(data_wrapper(data=data, success="true"))
        except:
            return Response(data_wrapper(msg=20001, success="false"))

    def put(self, request):
        namedict = {'problem_id': 20001, 'problem_type': 20001, 'title': 20001, 'time_limit': 20001,
                    'memory_limit': 20001, 'description': 20001, 'input': 20001, 'output': 20001,
                    'sample_output': 20001, 'sample_input': 20001, 'hint': 20001, 'source': 20001,
                    'defunct': 20001, 'tagids': 20001}
        params = get_params_from_post(request, namedict)
        params.pop('error') # if params['error']:
                                  # return Response(data_wrapper(success="false", msg=20001))
        try:
            tagids = json.loads(params.pop('tagids'))
            problem_type = int(params.pop('problem_type'))
            # 问题主要修改留给dealer做
            problem = self.dealer.edit(params, problem_type)
            # 修改问题的tag
            ori_tags = ProblemTag.objects.filter(problem_id=problem)
            ori_tags.delete()
            for id in tagids:
                tagid = Tags.objects.get(tagid=id)
                tag = ProblemTag.objects.create(problem_id=problem, tagid=tagid)
                tag.save()
            problem.save()
        except:
            return Response(data_wrapper(success="false", msg=20001))
        return Response(data_wrapper(data=self.get_serializer(problem).data, success="true"))

    def post(self, request):
        namedict = {'problem_type': 20001, 'title': 20001, 'time_limit': 20001,
                    'memory_limit': 20001, 'description': 20001, 'input': 20001, 'output': 20001,
                    'sample_output': 20001, 'sample_input': 20001, 'hint': 20001, 'source': 20001,
                    'defunct': 20001, 'tagids': 20001}
        params = get_params_from_post(request, namedict)
        params.pop('error')
        try:
            params['in_date'] = timezone.now()
            tagids = json.loads(params.pop('tagids'))
            problem_type = int(params['problem_type'])
            problem = self.dealer.create(params, problem_type)
            for id in tagids:
                tagid = Tags.objects.get(tagid=id)
                tag = ProblemTag.objects.create(problem_id=problem, tagid=tagid)
                tag.save()
            problem.save()
        except Exception as e:
            return Response(data_wrapper(success="false", msg=20001))
        return Response(data_wrapper(data=self.get_serializer(problem).data, success="true"))

