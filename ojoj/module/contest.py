from rest_framework import serializers
from rest_framework import generics
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.db import OperationalError
import datetime
import json
from json import JSONDecodeError
from .core import BaseListView
from ..utils import get_params_from_post, data_wrapper
from ..models import Contest, Problem, Users, ContestProblem, Solution, ContestFinish
from ..serializers import ContestSerializer, ContestDetailSerializer, ContestRankSerializer


class ContestView(BaseListView):
    queryset = Contest.objects.all().order_by('-contest_id')
    serializer_class = ContestSerializer
    pk_field = 'contest_id'

    def get_dataset(self, request):
        contest_id = request.GET.get('contest_id', None)
        type = request.GET.get('type', None)
        state = request.GET.get('state', None)

        try:
            dataset = self.queryset.all()
            if contest_id:
                dataset = dataset.filter(contest_id=contest_id)
            if type:
                dataset = dataset.filter(type=type)
            if state:
                dataset = dataset.filter(state=state)
            return dataset
        except:
            return dataset.none()

    def put(self, request):
        namedict = {'contest_id': 20001, 'type': 20001, 'title': 20001, 'begin': 20001, 'end': 20001,
                    'password': 20001, 'problem_list': 20001}
        params = get_params_from_post(request, namedict)
        if params.pop('error'):
            return Response(data_wrapper(msg=20001, success="false"))
        try:
            problem_list = json.loads(params.pop('problem_list'))
            contest = self.queryset.get(contest_id=params.pop('contest_id'))
            params['begin'] = datetime.datetime.strptime(params['begin'], "%Y-%m-%d %H:%M:%S")
            params['end'] = datetime.datetime.strptime(params['end'], "%Y-%m-%d %H:%M:%S")
            for key, value in params.items():
                setattr(contest, key, value)
            contest.save()
            # 删掉原来的竞赛题目关系，然后再新建
            ContestProblem.objects.filter(contest_id=contest).delete()
            for problem_id in problem_list:
                problem = Problem.objects.get(problem_id=problem_id)
                ContestProblem.objects.create(contest_id=contest, problem_id=problem).save()
        except ObjectDoesNotExist:
            return Response(data_wrapper(msg=20001, success="false"))
        except OperationalError:
            return Response(data_wrapper(msg=20001, success="false"))
        except JSONDecodeError:
            return Response(data_wrapper(success="false", msg=20001))
        return Response(data_wrapper(data=ContestDetailSerializer(contest).data, success="true"))

    def post(self, request):
        namedict = {'type': 20001, 'title': 20001, 'begin': 20001, 'end': 20001,
                    'uid': 20001, 'password': 20001, 'problem_list': 20001}
        params = get_params_from_post(request, namedict)
        if params.pop('error'):
            return Response(data_wrapper(msg=20001, success="false"))
        try:
            # pop掉problem_list不让他搞搞震
            problem_list = json.loads(params.pop('problem_list'))
            # 新建竞赛
            holder = Users.objects.get(uid=params.pop('uid'))
            params['holder'] = holder.uid
            params['begin'] = datetime.datetime.strptime(params['begin'], "%Y-%m-%d %H:%M:%S")
            params['end'] = datetime.datetime.strptime(params['end'], "%Y-%m-%d %H:%M:%S")
            params['score'] = 0
            contest = Contest.objects.create(**params)
            contest.save()
            # 搞搞竞赛与问题的关联
            for problem_id in problem_list:
                problem = Problem.objects.get(problem_id=problem_id)
                ContestProblem.objects.create(contest_id=contest, problem_id=problem).save()
        except ObjectDoesNotExist:
            return Response(data_wrapper(msg=20001, success="false"))
        except OperationalError:
            return Response(data_wrapper(msg=20001, success="false"))
        except JSONDecodeError:
            return Response(data_wrapper(success="false", msg=20001))
        return Response(data_wrapper(data=ContestDetailSerializer(contest).data, success="true"))


class ContestDetailView(generics.GenericAPIView):
    queryset = Contest.objects.all()
    serializer_class = ContestDetailSerializer

    def get(self, request):
        try:
            pwdFlag = True
            # 竞赛信息
            contest_id = request.GET['contest_id']
            password = request.GET.get('password', None)
            contest = self.queryset.get(contest_id=contest_id)
            data = self.get_serializer(contest).data
            # 验证密码
            if contest.password:
                if password != contest.password:
                    pwdFlag = False
            # 用户做题信息
            uid = request.GET.get('uid', None)
            if uid:
                user = Users.objects.get(uid=uid)
                # 暂时用来开给管理员
                if user.identity == '3':
                    pwdFlag = True
                user_info = {'accept_num': 0, 'accepted_problem': []}
                for problem in contest.problem_set.all():
                    if Solution.objects.filter(problem_id=problem.problem_id, uid=user.uid, result=4).exists():
                        user_info['accept_num'] = user_info['accept_num'] + 1
                        user_info['accepted_problem'].append(problem.problem_id)
                data['user_info'] = user_info
        except:
            return Response(data_wrapper(msg=20001, success="false"))
        if not pwdFlag: return Response(data_wrapper(msg=60003, success="false"))
        return Response(data_wrapper(success="true", data=data))


class ContestRankView(BaseListView):
    queryset = ContestFinish.objects.all()
    serializer_class = ContestRankSerializer

    def get_dataset(self, request):
        try:
            contest_id = request.GET['contest_id']
            dataset = self.queryset.filter(contest_id=contest_id).order_by('-accept_num', 'all_time')
            return dataset
        except:
            return self.queryset.none()