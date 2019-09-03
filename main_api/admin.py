from django.contrib import admin
from django import forms
# Register your models here.
from main_api.models import News, People, Software, SoftwareAuthors, Project, Research, CollaborationResearcher, \
    Collaboration, Highlight, Download


class NewsForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea, help_text='Note: You can enter text and HTML tags')

    class Meta:
        model = News
        fields = '__all__'


class NewsAdmin(admin.ModelAdmin):
    form = NewsForm


class SoftwareForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea, help_text='Note: You can enter text and HTML tags')

    class Meta:
        model = Software
        fields = '__all__'


class SoftwareAuthorsInline(admin.TabularInline):
    model = SoftwareAuthors
    extra = 1


class DownloadInline(admin.TabularInline):
    model = Download
    extra = 1


class SoftwareAdmin(admin.ModelAdmin):
    form = SoftwareForm
    inlines = (SoftwareAuthorsInline, DownloadInline)


class ProjectInline(admin.TabularInline):
    model = Project
    extra = 1


class ResearchAdmin(admin.ModelAdmin):
    inlines = (ProjectInline,)


class CollaboratorResearcherInline(admin.TabularInline):
    model = CollaborationResearcher
    extra = 1


class CollaborationAdmin(admin.ModelAdmin):
    inlines = (CollaboratorResearcherInline,)


class HighlightForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea, help_text='Note: You can enter text and HTML tags')
    subject = forms.CharField(widget=forms.Textarea, help_text='Note: You can enter text and HTML tags')

    class Meta:
        model = Highlight
        fields = '__all__'


class HighlightAdmin(admin.ModelAdmin):
    form = HighlightForm


admin.site.register(News, NewsAdmin)
admin.site.register(People)
admin.site.register(Software, SoftwareAdmin)
admin.site.register(Research, ResearchAdmin)
admin.site.register(Collaboration, CollaborationAdmin)
admin.site.register(Highlight, HighlightAdmin)
