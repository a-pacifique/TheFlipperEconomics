from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from PIL import Image
import os

class User(AbstractUser):
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.get_full_name()
    

class ResizedImageField(models.ImageField):
    def __init__(self, *args, **kwargs):
        self.width = kwargs.pop('width', None)
        self.height = kwargs.pop('height', None)
        super().__init__(*args, **kwargs)

    def save_form_data(self, instance, data):
        if data is not None:
            image = Image.open(data)
            if self.width is not None and self.height is not None:
                image = image.resize((self.width, self.height), Image.LANCZOS)
            else:
                if self.width is not None:
                    width, height = image.size
                    ratio = width / float(self.width)
                    new_height = int(height / ratio)
                    image = image.resize((self.width, new_height), Image.LANCZOS)
                elif self.height is not None:
                    width, height = image.size
                    ratio = height / float(self.height)
                    new_width = int(width / ratio)
                    image = image.resize((new_width, self.height), Image.LANCZOS)

            path = os.path.join(instance._meta.app_label, instance.__class__.__name__.lower())
            file_name = f"{instance.title.replace(' ', '_')}.jpg"
            file_path = os.path.join(self.upload_to, path, file_name)

            if not os.path.exists(os.path.dirname(file_path)):
                os.makedirs(os.path.dirname(file_path))

            with open(file_path, 'wb') as f:
                image.save(f, 'JPEG')

            file_name = os.path.join(path, file_name)
            setattr(instance, self.attname, file_name)

        super().save_form_data(instance, data)

class Article(models.Model):
    title = models.CharField(max_length=200)
    image = ResizedImageField(upload_to='articles/images/', verbose_name=_('article image'), width=800, height=600)
    content = models.TextField(verbose_name=_('article content'))
    date_written = models.DateTimeField(auto_now_add=True, verbose_name=_('date written'))
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('author'))
    views = models.IntegerField(default=0, verbose_name=_('views'))
    slug = models.SlugField(unique=True, max_length=200, blank=True)
    published = models.BooleanField(default=False, verbose_name=_('published'))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_written']
        verbose_name = _('article')
        verbose_name_plural = _('articles')

