from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='images_created', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField(max_length=2000)
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='images_liked', blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['-created']),
        ]
        ordering = ['-created']

    def __str__(self):
        return self.title

    # Мы переопределим метод save() модели Image, чтобы автоматически генерировать поля slug на основе значения поля title
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        '''Если при сохранении объекта Image поле slug является пустым, то slug генерируется автоматически из поля title изображения с по мощью функции
slugify(). Затем объект сохраняется. Благодаря автоматическому генерированию слага из заголовка пользователям не придется указывать слаг, когда
они делятся изображениями на сайте.
'''
