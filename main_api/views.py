import os

from django.core import serializers
from django.core.files.storage import default_storage
from django.db.models import Case, When
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse, Http404
from django.conf import settings
from bibtexparser.bparser import BibTexParser
import bibtexparser

import json

# Create your views here.
from main_api.models import News, People, Software, SoftwareAuthors


def news(request):
    news_data = News.objects.order_by('-pub_date').values()
    return JsonResponse(list(news_data), safe=False)


def people(request):
    people_data = People.objects.order_by('-join_date').values()
    people_data = modify_url(request, people_data, 'image')
    return JsonResponse(list(people_data), safe=False)


def modify_url(request, objects, key):
    media_url = 'http://' + request.get_host() + settings.MEDIA_URL
    for obj in objects:
        temp = obj[key]
        obj.update({key: media_url + temp})
    return objects


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


def software_list(request):
    soft_list = Software.objects.order_by('-pub_date').values()
    return JsonResponse(list(soft_list), safe=False)


def software(request, software_id):
    try:
        soft = Software.objects.filter(pk=software_id).values()
    except Software.DoesNotExist:
        raise Http404("Question does not exist")
    soft = modify_url(request, list(soft), 'detail')
    return JsonResponse(soft, safe=False)


def authors_of_software(request, software_id):
    authors = SoftwareAuthors.objects.filter(software__pk=software_id) \
        .order_by('order') \
        .values_list('author', flat=True)
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(authors)])
    people_data = People.objects.filter(id__in=authors).order_by(preserved).values()
    people_data = modify_url(request, people_data, 'image')
    return JsonResponse(list(people_data), safe=False)
