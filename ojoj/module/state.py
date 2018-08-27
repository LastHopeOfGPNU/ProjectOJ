from .core import BaseListView
from ..models import Solution, Users
from ..serializers import StateSerializer


class StateView(BaseListView):
    queryset = Solution.objects.all()
    serializer_class = StateSerializer

    def get_dataset(self, request):
        problem_id = request.GET.get('problem_id', None)
        nick = request.GET.get('nick', None)
        result = request.GET.get('result', None)
        dataset = self.queryset.filter(protype=3)

        try:
            if problem_id:
                dataset = dataset.filter(problem_id=problem_id)
            if nick:
                dataset = dataset.filter(uid__in=Users.objects.filter(nick=nick).values_list('uid', flat=True))
            if result:
                dataset = dataset.filter(result=result)
        except:
            return self.queryset.none()

        return dataset.order_by('-solution_id')