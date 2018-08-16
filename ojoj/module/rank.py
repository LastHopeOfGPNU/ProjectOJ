from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
import datetime
from django.utils import timezone
from .core import BaseListView
from ..utils import execute_raw_sql, data_wrapper
from ..models import Users
from ..serializers import RankUserSerializer


def get_rank_list(result_set):
    ret = []
    for i, row in enumerate(result_set):
        uid = row[0]
        ret.append({
            'uid': row[0],
            'nick': row[1],
            'count': row[2]
        })
    return ret

class RankView(GenericAPIView):

    # 返回日榜、月榜和总榜
    def get(self, request):
        count = request.GET.get('count', 6)  # 获取排行榜的条数，默认为6
        # 获取日榜、月榜和总榜的开始时间
        # 总榜假设由2015-01-01开始
        now = timezone.now()
        day = datetime.datetime(now.year, now.month, now.day, 0, 0, 0)
        month = datetime.datetime(now.year, now.month, 1, 0, 0, 0)
        all = datetime.datetime(2015, 1, 1, 0, 0, 0)
        # 由原OJ系统偷过来的神级SQL语句
        sql = "select solution.uid, users.nick, count(DISTINCT problem_id) as count from solution left join users on users.uid=solution.uid where result=4 and in_date>\'%s\' and in_date<\'%s\' group by uid order by count desc limit %d"

        try:
            count = int(count)
            # 执行SQL语句获取排行
            day_result = execute_raw_sql(sql % (day, now, count))  # 分别为（开始时间，结束时间，条数）
            month_result = execute_raw_sql(sql % (month, now, count))
            all_result = execute_raw_sql(sql % (all, now, count))
            data = {
                'today_list': get_rank_list(day_result),
                'month_list': get_rank_list(month_result),
                'all_list': get_rank_list(all_result)
            }
        except:
            return Response(data_wrapper(success="false", msg=20001))
        return Response(data_wrapper(data=data, success="true"))


class RankAllView(BaseListView):
    queryset = Users.objects.all().order_by('-solved')
    serializer_class = RankUserSerializer

