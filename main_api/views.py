import os

import bibtexparser
from bibtexparser.bparser import BibTexParser
from django.conf import settings
from django.core.files.storage import default_storage
from django.db.models import Case, When
from django.http import JsonResponse, Http404

# Create your views here.
from main_api.models import News, People, Software, SoftwareAuthors, Research, Collaboration, CollaborationResearcher, \
    Highlight


class BibHolder:
    Bib_Database = None
    Last_Change_Date = None


def news(request):
    news_list = News.objects.order_by('-pub_date').values()
    return JsonResponse(list(news_list), safe=False)


def people(request):
    people_data = People.objects.order_by('-join_date').values()
    people_data = add_media_url(request, people_data, 'image')
    return JsonResponse(list(people_data), safe=False)


def publications(request):
    update_bib_holder()
    return JsonResponse(BibHolder.Bib_Database.entries, safe=False)


def software_list(request):
    soft_list = Software.objects.order_by('-pub_date').values()
    return JsonResponse(list(soft_list), safe=False)


def software(request, software_id):
    try:
        soft = Software.objects.filter(pk=software_id).values()
    except Software.DoesNotExist:
        raise Http404("Question does not exist")
    soft = add_media_url(request, list(soft), 'detail')
    return JsonResponse(soft, safe=False)


def authors_of_software(request, software_id):
    authors = SoftwareAuthors.objects.filter(software__pk=software_id) \
        .order_by('order') \
        .values_list('author', flat=True)
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(authors)])
    people_data = People.objects.filter(id__in=authors).order_by(preserved).values()
    people_data = add_media_url(request, people_data, 'image')
    return JsonResponse(list(people_data), safe=False)


def add_media_url(request, objects, key):
    media_url = 'http://' + request.get_host() + settings.MEDIA_URL
    for obj in objects:
        temp = obj[key]
        obj.update({key: media_url + temp})
    return objects


def update_bib_holder():
    path = os.path.join(settings.MEDIA_ROOT, 'bibliography/bibliography.bib')
    current_last_change = os.path.getmtime(path)
    if BibHolder.Last_Change_Date != current_last_change:
        f = default_storage.open(path, 'r')
        bib_str = f.read()
        f.close()
        parser = BibTexParser()
        parser.ignore_nonstandard_types = True
        parser.homogenize_fields = False
        parser.common_strings = True
        BibHolder.Bib_Database = bibtexparser.loads(bib_str, parser)
        BibHolder.Last_Change_Date = current_last_change


def researches(request):
    researches_query = Research.objects.order_by('-date_added')
    research_list = researches_query.values()
    for research_q, research_o in zip(researches_query, research_list):
        projects = research_q.project_set.all().values()
        research_o.update({'projects': list(projects)})
    return JsonResponse(list(research_list), safe=False)


def collaborations(request):
    collaboration_list = Collaboration.objects.all().order_by('-start_date').values()
    for collaboration_o in collaboration_list:
        add_researchers_to_collaboration(collaboration_o)
    return JsonResponse(list(collaboration_list), safe=False)


def add_researchers_to_collaboration(collaboration_o):
    collaboration_o['researchers'] = []
    collaboration_researcher = CollaborationResearcher.objects.filter(collaboration=collaboration_o['id']) \
        .order_by('-start_date').values()
    for obj in collaboration_researcher:
        researcher = People.objects.filter(pk=obj['researcher_id']).values()[0]
        collaboration_o['researchers'].append({'field': obj['field'], 'people': researcher})


def highlights(request):
    highlight_list = Highlight.objects.all().values()
    return JsonResponse(list(highlight_list), safe=False)
