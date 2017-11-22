# -*- coding: utf_8 -*-
# import markdown

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.html import strip_tags

# Create your models here.

# 分类
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

# 标签
class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

# 文章
class Post(models.Model):
    title = models.CharField(max_length=70)
    body = models.TextField()
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    views = models.PositiveIntegerField(default=0)
    excerpt = models.CharField(max_length=200, blank=True)
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey(User)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-created_time']

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
    #     # 如果没有填写摘要
    #     if not self.excerpt:
    #         # 首先实例化一个 Markdown 类，用于渲染 body 的文本
    #         md = markdown.Markdown(extensions=[
    #             'markdown.extensions.extra',
    #             'markdown.extensions.codehilite',
    #         ])
    #         # 先将 Markdown 文本渲染成 HTML 文本
    #         # strip_tags 去掉 HTML 文本的全部 HTML 标签
    #         # 从文本摘取前 54 个字符赋给 excerpt
    #         self.excerpt = strip_tags(md.convert(self.body))[:54]

        # 调用父类的 save 方法将数据保存到数据库中
        super(Post, self).save(*args, **kwargs)

class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=225)
    url = models.URLField(blank=True)
    text = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)

    post = models.ForeignKey(Post)

    def __unicode__(self):
        return self.text[:20]

