from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
User = get_user_model()
from django.conf import settings


class BookStatuses(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="类别名称")
    parent = models.ForeignKey(
        'self',  # 关联自身
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name="subcategories"
    )

    def __str__(self):
        return f"{self.parent.name}/{self.name}" if self.parent else self.name

class NewBook(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # 指向当前使用的用户模型
        on_delete=models.CASCADE,
        related_name='books', # 可选：用于从用户对象反向获取书籍列表
        null=True, blank=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    publishyear = models.PositiveSmallIntegerField()
    statues = models.ForeignKey(BookStatuses,related_name='books', on_delete=models.CASCADE)
    language = models.CharField(max_length=200)
    pagenumber = models.PositiveIntegerField()
    cover = models.ImageField(upload_to='covers/', blank=True, null=True)
    # type = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='books',
        limit_choices_to={'parent__isnull': True}  # 只允许选择一级分类
    )
    subcategory = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='sub_books'
    )
    def __str__(self):
        category_name = self.category.name if self.category else "无分类"
        subcategory_name = self.subcategory.name if self.subcategory else ""
        return f"{self.title} ({category_name}/{subcategory_name})"


    # def __str__(self):
    #     return self.title


class EditExcerpt(models.Model):
    # 建立外键关系，确保当 Book 被删除时，相关的 Excerpt 也会被删除
    book = models.ForeignKey(NewBook, on_delete=models.CASCADE, related_name='excerpts',null=True)
    title = models.CharField("书摘标题", max_length=200, blank=True, null=True)
    content = models.TextField("书摘内容",null=True)
    feeling = models.TextField("书摘心得",null=True)
    page_number = models.PositiveIntegerField("页码", blank=True, null=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        if self.title:
            return f"{self.book.title} - {self.title}"
        return f"{self.book.title} - 未命名书摘"





