from django import forms
from django.contrib import admin
from pycotracker.models import Ticket, TicketVar, TicketConfig,\
                               TicketTag, TicketAssignement
from django.contrib.sites.models import get_current_site


class ConfigAdmin(admin.ModelAdmin):
    exclude = ('section',)
    list_display = ('key', 'value',)
    ordering = ('key',)
    def save_model(self, request, obj, form, change):
        obj.section = 'pycotracker'
        super(ConfigAdmin, self).save_model(request, obj, form, change)
admin.site.register(TicketConfig, ConfigAdmin)


class TicketVarForm(forms.ModelForm):
    value = forms.CharField(label='Value')
    class Meta:
        model = TicketVar

class TicketTagInline(admin.StackedInline):
    model = TicketTag
    extra = 0
    verbose_name = 'tags'
    exclude = ('key',)
    form = TicketVarForm

class TicketAssignementInline(admin.StackedInline):
    model = TicketAssignement
    extra = 0
    verbose_name = 'tags'
    exclude = ('key',)
    form = TicketVarForm

class TicketVarInline(admin.TabularInline):
    model = TicketVar
    extra = 0
    form = TicketVarForm
    def queryset(self, request):
        queryset = super(TicketVarInline, self).queryset(request)
        return queryset.exclude(key='tag').exclude(key='assignement')


class TicketModelForm(forms.ModelForm):
    STATUS_CHOICES = (
        (Ticket.STATUS_OPEN, 'Open'),
        (Ticket.STATUS_CLOSED, 'Closed'),
    )
    status = forms.ChoiceField(choices=STATUS_CHOICES)
    class Meta:
        model = Ticket

class TicketAdmin(admin.ModelAdmin):
    exclude = ('author', 'last_editor', 'sites', 'lang', 'encoding',
               'parent', 'type', 'date', 'format', )
    list_display = ('id', 'title', 'lang', 'status', 'author',
                    'date', 'last_date', )
    list_display_links = ('id', 'title', )
    list_filter = ('status', 'author', )
    inlines = (TicketAssignementInline, TicketTagInline, TicketVarInline,)
    ordering = ('-date',)
    form = TicketModelForm
    
    def save_model(self, request, obj, form, change):
        from django.conf import settings
        from django.utils import timezone
        obj.lang = settings.LANGUAGE_CODE
        obj.last_editor = request.user
        obj.last_date = timezone.now()
        if not change:
            obj.author = request.user
            obj.date = timezone.now()
        obj.format = 'raw'
        super(TicketAdmin, self).save_model(request, obj, form, change)
        
        if not change:
            obj.sites.add(get_current_site(request))

admin.site.register(Ticket, TicketAdmin)
