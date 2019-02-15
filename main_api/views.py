from django.http import HttpResponse, JsonResponse
from django.conf import settings

# Create your views here.
from main_api.models import News, People


def news(request):
    news_data = News.objects.order_by('-pub_date').values()
    return JsonResponse(list(news_data), safe=False)


def people(request):
    media_url = 'http://' + request.get_host() + settings.MEDIA_URL
    people_data = People.objects.order_by('-join_date').values()
    for person in people_data:
        temp = person['image']
        person.update({'image': media_url + temp})
    return JsonResponse(list(people_data), safe=False)
