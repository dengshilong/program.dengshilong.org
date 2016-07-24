title: Django之Q和F算子
date: 2016-07-24 08:50:02
tags:
    - Django
    - F
    - Q
categories:
    - 编程
---
Django提供了Q和F算子来方便查询。

### Q算子
在对queryset进行filter时，filter语句的关系是AND关系，要实现OR关系，则需要使用[Q算子](https://docs.djangoproject.com/en/1.9/topics/db/queries/#complex-lookups-with-q-objects)。

例如
```
Q(question__startswith='Who') | Q(question__startswith='What')
```
相当于
```
WHERE question LIKE 'Who%' OR question LIKE 'What%'
```
### F算子
在实际开发中，常常需要对数据库中的某一个字段进行加减操作，如评论数，访问量等等。一种做法是把这个字段读出来，然后进行操作，之后再保存到数据库中，而[F算子](https://docs.djangoproject.com/en/1.9/ref/models/expressions/#f-expressions)提供了简便的方法，它使这些操作直接在数据库中执行。
例如，在下面的例子中需要对stories_filed字段进行加1操作。
```
# Tintin filed a news story!
reporter = Reporters.objects.get(name='Tintin')
reporter.stories_filed += 1
reporter.save()
```
而使用F算子，则是
```
from django.db.models import F

reporter = Reporters.objects.filter(name='Tintin')
reporter.update(stories_filed=F('stories_filed') + 1)
```
F算子的优势在于不需要使用Python, 而只是使用数据库来完成操作。

而F算子的另外一个好处是减少多线程下的变量问题。
