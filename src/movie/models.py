from django.db import models
from django.utils.encoding import smart_text
from django.utils import timezone
from django.utils.text import slugify
from django.utils.timesince import timesince
from django.db.models.signals import post_save, pre_save
from datetime import timedelta, datetime, date
from .validators import Validate_studio

GENRE_CHOICES = (
('select', 'Select'),
('action', 'Action'),
('comedy', 'Comedy'),
('terror', 'Terror'),
('romance', 'Romance'),
('drama', 'Drama')
)

# Create your models here.
class MovieModelQuery(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def nuevo_title_items(self, value):
        return self.filter(title__icontains=value)

class MovieModelManager(models.Manager):
    def get_queryset(self):
        return MovieModelQuerySet(self.model, using = self._db)

        def all(self, *args, **kwargs):
            qs = super(MovieModelManager, self).all(*args, **kwargs).active()
            return qs

class Movie(models.Model):
    name = models.CharField(max_length = 120)
    year = models.CharField(max_length = 120, blank = True, null = True)
    studio = models.CharField(max_length = 120, validators = [Validate_studio], null = True, blank = True)
    genre = models.CharField(max_length = 120, choices = GENRE_CHOICES, default = "select")
    slug = models.SlugField(null = True, blank = True)
    active = models.BooleanField(default = True)
    created = models.DateField(auto_now = False, auto_now_add = False, default = timezone.now)
    updated = models.DateTimeField(auto_now = True)
    timestamp = models.DateTimeField(auto_now_add = True)

    objects = MovieModelManager

    def __str__(self):
        return smart_text(self.name)

    def save(self, *args, **kwargs):
        print ("Guarde algo")
        if not self.slug:
            if self.name:
                self.slug = slugify(self.name)
                super(Movie, self).save(*args, **kwargs)

    @property
    def age(self):
        if self.created == 'Create':
            now = datetime.now()
            created = datetime.combine(self.created, datetime.now().min.time()
            )

        try:
            difference = now - created
            print(difference)
        except:
            difference = "No hay creacion"

        if difference <= datetime.timedelta(minutes = 1):
            print (difference)
            return "Ahora"
        return "{time} ago", format(time = timestamp(created).split(",")[0])

def movie_model_post_save_receiver(sender, instance, *args, **kwargs):
    print("Despues almacenar")
    if not instance.slug and instance.name:
        instance.slug = slugify(instance.name)
        instance.save()
post_save.connect(movie_model_post_save_receiver, sender = Movie)

def movie_pre_save_receiver(sender, instance, *args, **kwargs):
    print ("Antes de almacenar")
    if not instance.slug and instance.name:
        instance.slug = slugify(instance.name)
        instance.save()
pre_save.connect(movie_model_post_save_receiver, sender = Movie)
