title: Django-REST-framework嵌套序列化过滤
date: 2018-08-09 20:26:26
tags:
    - Django
categories:
---
有些时候，需要用到嵌套过滤，例如如果要求数据都只是逻辑删除时，此时就会用到。例如有一个应用表，还有一个应用成员表, 如果显示应用详情时，想在一个接口把应用成员一起显示出来，此时就需要过滤掉那些被逻辑删除的成员。

如下定义的application和member

```
class Application(models.Model):
    """应用"""

    name = models.CharField(max_length=32, help_text='应用名称')
    is_deleted = models.BooleanField(default=False, help_text='是否已删除')
    gmt_create = models.DateTimeField(auto_now_add=True)
    gmt_modify = models.DateTimeField(auto_now=True)

class Member(models.Model):
    """应用成员"""

    application = models.ForeignKey(Application, help_text='应用', related_name='members', on_delete=models.PROTECT, db_constraint=False)
    user = models.ForeignKey(User, help_text='成员', on_delete=models.PROTECT, db_constraint=False)
    is_deleted = models.BooleanField(default=False, help_text='是否已删除')
    gmt_create = models.DateTimeField(auto_now_add=True)
    gmt_modify = models.DateTimeField(auto_now=True)
```

序列化如下

```
class MemberSerializer(Serializer):
    '''应用成员 序列化器'''

    class Meta:
        model = Member
        fields = '__all__'
        read_only_fields = ('gmt_create', 'gmt_modify', 'is_deleted')


class ApplicationDetailSerializer(Serializer):
    members = MemberSerializer(many=True)

    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ('gmt_create', 'gmt_modify', 'is_deleted')
```

此时会把应用中逻辑删除掉的用户也查出来，查看[How do you filter a nested serializer in Django Rest Framework?](https://stackoverflow.com/questions/28163556/how-do-you-filter-a-nested-serializer-in-django-rest-framework/28354281#28354281)得到解答。需要在Meta中添加list_serializer_class, 修改后如下

```
class DeletedFilterListSerializer(ListSerializer):

    def to_representation(self, data):
        data = data.filter(is_deleted=False)
        return super(DeletedFilterListSerializer, self).to_representation(data)


class MemberSerializer(Serializer):
    '''应用成员 序列化器'''

    class Meta:
        list_serializer_class = DeletedFilterListSerializer
        model = Member
        fields = '__all__'
        read_only_fields = ('gmt_create', 'gmt_modify', 'is_deleted')
```

如此序列化应用时，就不会把删除掉的应用成员查出来
