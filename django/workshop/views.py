# coding: utf-8

from django.views.generic import ListView, DetailView

from models import Workshop


class WorkshopList(ListView):
    model = Workshop
    template_name = 'lista.html'
    context_object_name = 'workshops'


class WorkshopDetail(DetailView):
    model = Workshop
    template_name = 'detalhe.html'
    context_object_name = 'workshop'
