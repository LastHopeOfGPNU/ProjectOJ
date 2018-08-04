from rest_framework import generics
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.db import OperationalError
from .core import BaseListView
from ..utils import data_wrapper, get_params_from_post
from ..models import Problem, Solution, Users, ProblemTag
from ..serializers import ProblemSerializer, SolutionSerializer, ProblemDetailSerializer
import json
from json.decoder import JSONDecodeError


class ProblemView(BaseListView):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer

    def delete(self, request):
        try:
            problem_id = request.GET.get('problem_id')
            problem = self.get_queryset().get(problem_id=problem_id)
            # 删除问题
            problem.delete()
            # 删除问题相关solution
            solutions = Solution.objects.filter(problem_id=problem_id)
            solutions.delete()
            # TODO: 删除相关数据文件
        except KeyError:
            return Response(data_wrapper(success="false", msg=20001))
        except ObjectDoesNotExist:
            return Response(data_wrapper(success="false", msg=20001))
        return Response(data_wrapper(success="true"))

    def get_dataset(self, request):
        title = request.GET.get('title', None)
        problem_id = request.GET.get('problem_id', None)
        problem_type = request.GET.get('problem_type', None)
        tagid = request.GET.get('tagid', None)
        defunct = request.GET.get('defunct', None)
        dataset = self.get_queryset()

        if tagid:
            dataset = dataset.filter(tags__tagid=tagid)
        if title:
            print("title:", title)
            dataset = dataset.filter(title=title)
        if problem_id:
            dataset = dataset.filter(problem_id=problem_id)
        if problem_type:
            dataset = dataset.filter(problem_type=problem_type)
        if defunct:
            dataset = dataset.filter(defunct=defunct)

        return dataset.filter(is_verify=1).order_by('problem_id')


class ProblemDetailView(generics.GenericAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemDetailSerializer

    def get(self, request):
        try:
            uid = request.GET['uid']
            problem_id = request.GET['problem_id']

            problem = self.get_queryset().get(problem_id=problem_id)
            prob_ser = ProblemDetailSerializer(problem)
            user = Users.objects.get(uid=uid)
            # 取最新的solution
            solution = Solution.objects.filter(uid=user.uid, problem_id=problem_id).order_by('-solution_id')
            if solution.exists():
                solution = solution[0]
            else:
                solution = None
            solu_ser = SolutionSerializer(solution)
            data = prob_ser.data
            data.update(solu_ser.data)
            return Response(data_wrapper(data=data, success="true"))
        except KeyError:
            return Response(data_wrapper(msg=20001, success="false"))
        except ObjectDoesNotExist:
            return Response(data_wrapper(msg=20001, success="false"))

    def put(self, request):
        namedict = {'problem_id': 20001, 'problem_type': 20001, 'title': 20001, 'time_limit': 20001,
                    'memory_limit': 20001, 'description': 20001, 'input': 20001, 'output': 20001,
                    'sample_output': 20001, 'sample_input': 20001, 'hint': 20001, 'source': 20001,
                    'spj': 20001, 'defunct': 20001, 'tagids': 20001}
        params = get_params_from_post(request, namedict)
        if params['error']:
            return Response(data_wrapper(success="false", msg=20001))
        try:
            problem = self.queryset.get(problem_id=params['problem_id'])
            for key, value in params.items():
                if key == 'tagids':
                    tagids = json.loads(value)
                    ori_tags = ProblemTag.objects.filter(problem_id=params['problem_id'])
                    ori_tags.delete()
                    for id in tagids:
                        tag = ProblemTag.objects.create(problem_id=params['problem_id'], tagid=id)
                        tag.save()
                else:
                    setattr(problem, key, value)
            problem.save()
        except ObjectDoesNotExist:
            return Response(data_wrapper(success="false", msg=20001))
        except OperationalError:
            return Response(data_wrapper(success="false", msg=20001))
        except JSONDecodeError:
            return Response(data_wrapper(success="false", msg=20001))
        return Response(data_wrapper(data=self.get_serializer(problem).data, success="true"))



