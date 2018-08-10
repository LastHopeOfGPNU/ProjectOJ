from rest_framework import generics
from rest_framework.response import Response
from django.db import OperationalError
from django.core.exceptions import ObjectDoesNotExist
from ..utils import data_wrapper, get_params_from_post
from ..models import Tags
from ..serializers import TagSerializer

def get_children_tree(parent):
    ret = {}
    children = Tags.objects.filter(pid=parent.tagid).order_by('tagid')
    for child in children:
        ret[child.tagid] = get_children_tree(child)
    return ret

def delete_tag(tag):
    children = Tags.objects.filter(pid=tag.tagid)
    tag.delete()
    for child in children:
        delete_tag(child)

class TagView(generics.GenericAPIView):
    queryset = Tags.objects.all()
    serializer_class = TagSerializer

    def get(self, request):
        tag_tree = {}
        tag_dict = {}
        parents = self.queryset.filter(pid=-1).order_by('tagid')
        for parent in parents:
            tag_tree[parent.tagid] = get_children_tree(parent)
        for tag in self.queryset.all().order_by('tagid'):
            tag_dict[tag.tagid] = tag.tagname
        data = {
            'tag_tree': tag_tree,
            'tag_dict': tag_dict
        }
        return Response(data_wrapper(data=data, success="true"))

    def post(self, request):
        namedict = {'tagname': 20001, 'pid': 20001}
        params = get_params_from_post(request, namedict)
        if params.pop('error'):
            return Response(data_wrapper(msg=20001, success="false"))
        try:
            tag = Tags.objects.create(**params)
            tag.save()
        except OperationalError:
            return Response(data_wrapper(msg=20001, success="false"))
        return Response(data_wrapper(data=self.get_serializer(tag).data, success="true"))

    def put(self, request):
        namedict = {'tagid': 20001, 'tagname': 20001, 'pid': 20001}
        params = get_params_from_post(request, namedict)
        if params.pop('error'):
            return Response(data_wrapper(msg=20001, success="true"))
        try:
            tag = self.queryset.get(tagid=params.pop('tagid'))
            for key, value in params.items():
                setattr(tag, key, value)
            tag.save()
        except ObjectDoesNotExist:
            return Response(data_wrapper(msg=20001, success="false"))
        except OperationalError:
            return Response(data_wrapper(msg=20001, success="false"))
        return Response(data_wrapper(data=self.get_serializer(tag).data, success="true"))

    def delete(self, request):
        # 需要级联删除子标签
        try:
            tagid = request.GET['tagid']
            tag = self.queryset.get(tagid=tagid)
            delete_tag(tag)
        except KeyError:
            return Response(data_wrapper(msg=20001, success="false"))
        except ObjectDoesNotExist:
            return Response(data_wrapper(msg=20001, success="false"))
        except OperationalError:
            return Response(data_wrapper(msg=20001, success="false"))
        return Response(data_wrapper(success="true"))
