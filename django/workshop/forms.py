# coding: utf-8
from django import forms

from models import Workshop, Participante


class WorkshopForm(forms.ModelForm):

    class Meta:
        model = Workshop
        fields = '__all__'

    def clean(self):
        workshop = super(WorkshopForm, self).clean()

        if self.instance.pk:
            quantidade_inscritos = self.instance.participantes.count()
            novo_numero_vagas = workshop.get('vagas')
            if quantidade_inscritos > novo_numero_vagas:
                raise forms.ValidationError(
                    u'O workshop "{}" já possui "{}" inscritos. Por favor, informe uma quantidade de vagas maior ou igual a "{}".'.format(workshop.get('nome'), quantidade_inscritos, quantidade_inscritos)
                )
        return workshop


class ParticipanteForm(forms.ModelForm):

    workshops = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        queryset=Workshop.objects.all()
    )

    class Meta:
        model = Participante
        fields = '__all__'

    def clean(self):
        participante = super(ParticipanteForm, self).clean()
        workshop_selecionado = participante.get('workshops', ())

        for workshop in workshop_selecionado:
            if workshop.participantes.count() >= workshop.vagas:
                raise forms.ValidationError(
                    u'O workshop "{}" já está lotado.'.format(workshop.nome)
                )

        return participante
