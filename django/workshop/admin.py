from django.contrib import admin

from models import Workshop, Participante


class WorkshopAdmin(admin.ModelAdmin):
    search_fields = ('nome', )
    actions = None
    prepopulated_fields = {'slug': ('nome',)}


class ParticipanteAdmin(admin.ModelAdmin):
    list_filter = ('workshops__nome',)
    search_fields = ('nome', )
    actions = None

admin.site.register(Workshop, WorkshopAdmin)
admin.site.register(Participante, ParticipanteAdmin)
