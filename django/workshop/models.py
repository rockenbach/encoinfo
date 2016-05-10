from __future__ import unicode_literals

from django.db import models


class Workshop(models.Model):
    nome = models.CharField(u'Nome', max_length=200)
    slug = models.SlugField(u'Slug', max_length=200)
    vagas = models.IntegerField(u'Quantidade de vagas')

    def __unicode__(self):
        return '{}'.format(self.nome)


class Participante(models.Model):
    nome = models.CharField(u'Nome', max_length=200)
    idade = models.IntegerField(u'Idade', null=True, blank=True)
    cpf = models.IntegerField(u'CPF', unique=True)
    workshops = models.ManyToManyField(Workshop, blank=True, related_name='participantes')

    def __unicode__(self):
        return u'{}'.format(self.nome)
