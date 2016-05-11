from django.contrib import admin

from models import Workshop, Participante
# import os forms criados
from forms import WorkshopForm, ParticipanteForm


class WorkshopAdmin(admin.ModelAdmin):
    form = WorkshopForm
    search_fields = ('nome', )
    actions = None
    prepopulated_fields = {'slug': ('nome',)}


class ParticipanteAdmin(admin.ModelAdmin):
    form = ParticipanteForm
    list_filter = ('workshops__nome',)
    search_fields = ('nome', )
    actions = None

admin.site.register(Workshop, WorkshopAdmin)
admin.site.register(Participante, ParticipanteAdmin)
