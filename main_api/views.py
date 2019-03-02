import os

from django.core.files.storage import default_storage
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from bibtexparser.bparser import BibTexParser
import bibtexparser

import json

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


def publications(request):
    f = default_storage.open(os.path.join(settings.MEDIA_ROOT, 'bib/biblio.bib'), 'r')
    bib_str = f.read()
    f.close()
    parser = BibTexParser()
    parser.ignore_nonstandard_types = True
    parser.homogenize_fields = False
    parser.common_strings = True
    bib_database = bibtexparser.loads(bib_str, parser)
    return JsonResponse(bib_database.entries, safe=False)
