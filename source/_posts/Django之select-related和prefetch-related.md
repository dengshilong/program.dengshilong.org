title: Django之select_related和prefetch_related
date: 2016-07-24 14:20:04
tags:
    - Django
    - Python
    - select_related
    - prefetch_related
categories:
    - Python
---
在Django中，使用[select_related](https://docs.djangoproject.com/en/1.9/ref/models/querysets/#select-related)和[prefetch_related](https://docs.djangoproject.com/en/1.9/ref/models/querysets/#django.db.models.query.QuerySet.prefetch_related)是两个很常见的优化手段。

举个例子最能说明问题。

### 准备工作
首先建立如下model
```
class Category(models.Model):
    name = models.CharField(max_length=30)
    creat_time = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return u'%s' % self.name

class Tag(models.Model):
    name = models.CharField(max_length=30)
    creat_time = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return u'%s' % self.name

class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=300, allow_unicode=True, unique=True)
    content = models.TextField()
    publish_time = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category)
    tag = models.ManyToManyField(Tag, blank=True)

    def __unicode__(self):
        return u'%s' % self.title
```
之后编写序列化
```
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag


class PostSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    tag = TagSerializer(many=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'slug', 'content', 'publish_time', 'category', 'tag', )
```
之后编写api
```

class PostListAPI(generics.ListAPIView):
    serializer_class = PostSerializer
    model = Post
    paginate_by = 10


    def get_queryset(self):
        return Post.objects.all().order_by('-publish_time')
```
编写url
```
    url(r'^api/posts/?$', PostListAPI.as_view(), name='post_list'),
```

之后在后台新建两篇文章，访问api, 可以看到访问的sql
```
DEBUG [24/Jul/2016 13:57:13] [django.db.backends:utils:execute:89] [None] (0.000) SELECT "blog_post"."id", "blog_post"."title", "blog_post"."slug", "blog_post"."content", "blog_post"."publish_time", "blog_post"."category_id" FROM "blog_post" ORDER BY "blog_post"."publish_time" DESC; args=()
DEBUG [24/Jul/2016 13:57:13] [django.db.backends:utils:execute:89] [None] (0.000) SELECT "blog_category"."id", "blog_category"."name", "blog_category"."creat_time" FROM "blog_category" WHERE "blog_category"."id" = 1; args=(1,)
DEBUG [24/Jul/2016 13:57:13] [django.db.backends:utils:execute:89] [None] (0.000) SELECT "blog_tag"."id", "blog_tag"."name", "blog_tag"."creat_time" FROM "blog_tag" INNER JOIN "blog_post_tag" ON ("blog_tag"."id" = "blog_post_tag"."tag_id") WHERE "blog_post_tag"."post_id" = 2; args=(2,)
DEBUG [24/Jul/2016 13:57:13] [django.db.backends:utils:execute:89] [None] (0.000) SELECT "blog_category"."id", "blog_category"."name", "blog_category"."creat_time" FROM "blog_category" WHERE "blog_category"."id" = 1; args=(1,)
DEBUG [24/Jul/2016 13:57:13] [django.db.backends:utils:execute:89] [None] (0.000) SELECT "blog_tag"."id", "blog_tag"."name", "blog_tag"."creat_time" FROM "blog_tag" INNER JOIN "blog_post_tag" ON ("blog_tag"."id" = "blog_post_tag"."tag_id") WHERE "blog_post_tag"."post_id" = 1; args=(1,)
```
这里有两篇文章，访问tag和category表都分别访问了两次，如果是10篇文章，那访问tag和category则分别要10次。此时select_related和prefetch_related派上了用场。

### select_related
查看[select_related](https://docs.djangoproject.com/en/1.9/ref/models/querysets/#select-related)的文档，在返回QuerySet时，对于ForeignKey和OneToOneField等字段，通过添加select_related，可以把相关的对象在一次查询中查出，之后使用时就不需要再次查数据库。

还是看例子容易明白。对于上面的Post中category字段，因为是ForeignKey, 所以可以通过select_related查出，修改api如下
```

class PostListAPI(generics.ListAPIView):
    serializer_class = PostSerializer
    model = Post
    paginate_by = 10


    def get_queryset(self):
        queryset = Post.objects.all().order_by('-publish_time')
        queryset = queryset.select_related('category')
        return queryset
```
访问url, 查看sql
```
DEBUG [24/Jul/2016 13:58:29] [django.db.backends:utils:execute:89] [None] (0.000) SELECT "blog_post"."id", "blog_post"."title", "blog_post"."slug", "blog_post"."content", "blog_post"."publish_time", "blog_post"."category_id", "blog_category"."id", "blog_category"."name", "blog_category"."creat_time" FROM "blog_post" INNER JOIN "blog_category" ON ("blog_post"."category_id" = "blog_category"."id") ORDER BY "blog_post"."publish_time" DESC; args=()
DEBUG [24/Jul/2016 13:58:29] [django.db.backends:utils:execute:89] [None] (0.000) SELECT "blog_tag"."id", "blog_tag"."name", "blog_tag"."creat_time" FROM "blog_tag" INNER JOIN "blog_post_tag" ON ("blog_tag"."id" = "blog_post_tag"."tag_id") WHERE "blog_post_tag"."post_id" = 2; args=(2,)
DEBUG [24/Jul/2016 13:58:29] [django.db.backends:utils:execute:89] [None] (0.000) SELECT "blog_tag"."id", "blog_tag"."name", "blog_tag"."creat_time" FROM "blog_tag" INNER JOIN "blog_post_tag" ON ("blog_tag"."id" = "blog_post_tag"."tag_id") WHERE "blog_post_tag"."post_id" = 1; args=(1,)
```
可以看到，对于category信息，在查询post的同时，也一起查出，减少了查询category表的操作。

### prefetch_related
查看Django的[prefetch_related](https://docs.djangoproject.com/en/1.9/ref/models/querysets/#prefetch-related)文档，了解到prefetch_related对于相关对象会进行一次独立的查询，然后在Python中把对象关联起来。所以prefetch_related可以用于many-to-many and many-to-one关系。

还是举例子，对于上面的tag, 可以使用prefetch_related来处理。修改api如下:
```
class PostListAPI(generics.ListAPIView):
    serializer_class = PostSerializer
    model = Post
    paginate_by = 10


    def get_queryset(self):
        queryset = Post.objects.all().order_by('-publish_time')
        queryset = queryset.select_related('category')
        queryset = queryset.prefetch_related('tag')
        return queryset
```
之后访问api,查看sql
```
DEBUG [24/Jul/2016 14:02:35] [django.db.backends:utils:execute:89] [None] (0.000) SELECT "blog_post"."id", "blog_post"."title", "blog_post"."slug", "blog_post"."content", "blog_post"."publish_time", "blog_post"."category_id", "blog_category"."id", "blog_category"."name", "blog_category"."creat_time" FROM "blog_post" INNER JOIN "blog_category" ON ("blog_post"."category_id" = "blog_category"."id") ORDER BY "blog_post"."publish_time" DESC; args=()
DEBUG [24/Jul/2016 14:02:35] [django.db.backends:utils:execute:89] [None] (0.000) SELECT ("blog_post_tag"."post_id") AS "_prefetch_related_val_post_id", "blog_tag"."id", "blog_tag"."name", "blog_tag"."creat_time" FROM "blog_tag" INNER JOIN "blog_post_tag" ON ("blog_tag"."id" = "blog_post_tag"."tag_id") WHERE "blog_post_tag"."post_id" IN (2, 1); args=(2, 1)
```
可以看到对于tag的查询也只有一次。

从上面的例子可以看到，掌握select_related和prefetch_related的用法非常重要。本文的代码见[test-django](https://github.com/dengshilong/test-django)的blog

参看资料：
* http://blog.jobbole.com/74881/
