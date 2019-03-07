from django.contrib import admin
from django import forms
# Register your models here.
from main_api.models import News, People, Software, SoftwareAuthors


class NewsForm(forms.ModelForm):
    news_text = forms.CharField(widget=forms.Textarea, help_text='Note: You can enter text and HTML tags')

    class Meta:
        model = News
        fields = '__all__'


class NewsAdmin(admin.ModelAdmin):
    form = NewsForm


class SoftwareForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea, help_text='Note: You can enter text and HTML tags')

    class Meta:
        model = News
        fields = '__all__'


class SoftwareAuthorsInline(admin.TabularInline):
    model = SoftwareAuthors
    extra = 1


class SoftwareAdmin(admin.ModelAdmin):
    form = SoftwareForm
    inlines = (SoftwareAuthorsInline,)


admin.site.register(News, NewsAdmin)
admin.site.register(People)
admin.site.register(Software, SoftwareAdmin)
