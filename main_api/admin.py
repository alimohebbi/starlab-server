from django.contrib import admin
from django import forms
# Register your models here.
from main_api.models import News, People, Software, SoftwareAuthors


class NewsForm(forms.ModelForm):
    news_text = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = News
        fields = '__all__'


class NewsAdmin(admin.ModelAdmin):
    form = NewsForm


class SoftwareAuthorsInline(admin.TabularInline):
    model = SoftwareAuthors
    extra = 1


class SoftwareAdmin(admin.ModelAdmin):
    inlines = (SoftwareAuthorsInline, )


admin.site.register(News, NewsAdmin)
admin.site.register(People)
admin.site.register(Software, SoftwareAdmin)
