from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


# Create your models here.

class PublishedManager(models.Manager):
    """менеджер для извлечения опубликованных постов"""

    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    """Позволит хранить посты блога в базе данных"""

    class Status(models.TextChoices):
        """статус поста"""
        # черновик
        DRAFT = 'DF', 'Draft'
        # опубликован
        PUBLISHED = 'PB', 'Published'

    # заголовок
    title = models.CharField(max_length=250)

    # короткая метка
    # уникальная для даты публикации
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    # автор поста
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    # тело поста
    body = models.TextField()

    # дата публикации
    publish = models.DateTimeField(default=timezone.now)

    # дата создания
    created = models.DateTimeField(auto_now_add=True)

    # дата изменения
    update = models.DateTimeField(auto_now=True)

    # статус
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)

    objects = models.Manager()  # менеджер, применяемый по умолчанию
    published = PublishedManager()  # конкретно-прикладной менеджер

    class Meta:
        """сортировка по дате публикации в убывающем порядке"""
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]

    def __str__(self):
        """возвращает заголовок"""
        return self.title

    def get_absolute_url(self):
        """ Канонический URL-адрес
        reverse будет формировать URL-адрес динамически, применяя
        имя URL-адреса, определенное в шаблонах URL-адресов"""
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])
