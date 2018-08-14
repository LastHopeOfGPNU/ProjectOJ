from rest_framework import generics
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.db import OperationalError, DataError
from django.utils import timezone
from .core import BaseListView
from ..utils import data_wrapper, get_params_from_post
from ..models import Problem, Solution, Users, ProblemTag, Tags
from ..serializers import ProblemSerializer, SolutionSerializer, ProblemDetailSerializer
import json
from json.decoder import JSONDecodeError


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
        except KeyError:
            return Response(data_wrapper(success="false", msg=20001))
        except ObjectDoesNotExist:
            return Response(data_wrapper(success="false", msg=20001))
        except OperationalError:
            return Response(data_wrapper(success="false", msg=20001))
        return Response(data_wrapper(success="true"))

    def get_dataset(self, request):
        title = request.GET.get('title', None)
        problem_id = request.GET.get('problem_id', None)
        problem_type = request.GET.get('problem_type', None)
        tagid = request.GET.get('tagid', None)
        defunct = request.GET.get('defunct', None)
        accept_rate = request.GET.get('accept_rate', None)
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
        if accept_rate:
            if accept_rate.lower() == 'desc':
                dataset = dataset.order_by('-accept_rate')
            elif accept_rate.lower() == 'asc':
                dataset = dataset.order_by('accept_rate')
        if finished_by:
            solution = Solution.objects.filter(uid=finished_by)
            dataset = dataset.filter(problem_id__in=solution.values_list('problem_id', flat=True))

        return dataset.filter(is_verify=1)


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
            params.pop('problem_id')
            params['in_date'] = timezone.now()
            for key, value in params.items():
                if key == 'tagids':
                    tagids = json.loads(value)
                    ori_tags = ProblemTag.objects.filter(problem_id=problem)
                    ori_tags.delete()
                    for id in tagids:
                        tagid = Tags.objects.get(tagid=id)
                        tag = ProblemTag.objects.create(problem_id=problem, tagid=tagid)
                        tag.save()
                else:
                    setattr(problem, key, value)
            problem.save()
        except ObjectDoesNotExist:
            return Response(data_wrapper(success="false", msg=20001))
        except OperationalError:
            return Response(data_wrapper(success="false", msg=20001))
        except DataError:
            return Response(data_wrapper(success="false", msg=20001))
        except JSONDecodeError:
            return Response(data_wrapper(success="false", msg=20001))
        return Response(data_wrapper(data=self.get_serializer(problem).data, success="true"))

    def post(self, request):
        namedict = {'problem_type': 20001, 'title': 20001, 'time_limit': 20001,
                    'memory_limit': 20001, 'description': 20001, 'input': 20001, 'output': 20001,
                    'sample_output': 20001, 'sample_input': 20001, 'hint': 20001, 'source': 20001,
                    'spj': 20001, 'defunct': 20001, 'tagids': 20001}
        params = get_params_from_post(request, namedict)
        if params.pop('error'):
            return Response(data_wrapper(success="false", msg=20001))
        try:
            params['in_date'] = timezone.now()
            tagids = json.loads(params.pop('tagids'))
            problem = Problem.objects.create(**params)
            for id in tagids:
                tagid = Tags.objects.get(tagid=id)
                tag = ProblemTag.objects.create(problem_id=problem, tagid=tagid)
                tag.save()
            problem.save()
        except ObjectDoesNotExist:
            return Response(data_wrapper(success="false", msg=20001))
        except OperationalError:
            return Response(data_wrapper(success="false", msg=20001))
        except DataError:
            return Response(data_wrapper(success="false", msg=20001))
        except JSONDecodeError:
            return Response(data_wrapper(success="false", msg=20001))
        return Response(data_wrapper(data=self.get_serializer(problem).data, success="true"))

