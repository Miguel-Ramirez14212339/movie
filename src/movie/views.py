# Create your views here.
from django.shortcuts import render
from django.shortcuts import redirect
from .models import Movie
import redis
from django.contrib import messages
from django.contrib.messages import get_messages

r = redis.Redis(host='localhost', port=6379, db=0)
# Create your views here.
def sql_to_redis(request):
    ##r = redis.Redis(host='localhost', port=6379, db=0)
    ##m = Movie.objects.all()

    film = {"Movies": { }
    }

    Cinema = []
    data_origin = []

    for i in list(Movie.objects.all()):
        film ["Movies"].update({
        i.id : {
        "name": i.name,
        "year": i.year,
        "studio": i.studio,
        "genre": i.genre,
        "active": i.active,
        "created": i.created } })

        r.sadd("DBstorage:Movies:{}".format(i.id), film["Movies"][i.id])
        data_origin = list((r.smembers("DBstorage:Movies:{}".format(i.id))))
        Cinema.append(str (data_origin[0].decode('UTF-8')))
    print(Cinema)
    message = str(Cinema)
    messages.add_message(request, messages.INFO, message)
    return redirect('/')

def home(request, **kwargs):
            dato = []

            for message in messages.get_messages(request):
                dato=message
                break

            return render(request, 'index.html', context={'valor':dato})
