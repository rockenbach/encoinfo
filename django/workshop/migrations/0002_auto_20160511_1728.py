# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-11 17:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Participante',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200, verbose_name='Nome')),
                ('idade', models.IntegerField(blank=True, null=True, verbose_name='Idade')),
                ('cpf', models.IntegerField(unique=True, verbose_name='CPF')),
            ],
        ),
        migrations.AddField(
            model_name='workshop',
            name='descricao',
            field=models.TextField(blank=True, null=True, verbose_name='Descri\xe7\xe3o'),
        ),
        migrations.AddField(
            model_name='participante',
            name='workshops',
            field=models.ManyToManyField(blank=True, related_name='participantes', to='workshop.Workshop'),
        ),
    ]
