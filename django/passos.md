# Descrição
Sistema para gerenciar as inscrições nos minicursos do próximo encoinfo.
* o admin do django será utilizado pelos organizadores para realizar a inscrição dos participantes;

## Criando o projeto:

    django-admin startproject encoinfo .

Após criar o projeto:
* defina o idioma do projeto para português:
    * [Documentação 'LANGUAGE_CODE'](https://docs.djangoproject.com/en/1.9/ref/settings/#language-code)
    * LANGUAGE_CODE = 'pt-BR'
* desative o uso de fuso-horário (USE_TZ = False)
    * [Documentação 'TIMEZONE'](https://docs.djangoproject.com/en/1.9/ref/settings/#std:setting-TIME_ZONE)
    * [Documentação 'USE_TZ'](https://docs.djangoproject.com/en/1.9/ref/settings/#use-tz)
    * USE_TZ = False

## Criado o app workshop

    django-admin startapp workshop

Note que a estrutura criada é diferente da estrutura gerada pelo comando 'startproject'.

## Criando models e migrações

Crie o model 'Workshop' em 'workshop/models.py':

    # workshop/models.py
    class Workshop(models.Model):
        nome = models.CharField(u'Nome', max_length=200)
        slug = models.SlugField(u'Slug', max_length=200)
        vagas = models.IntegerField(u'Quantidade de vagas')

        def __unicode__(self):
            return '{}'.format(self.nome)


Adicione o app 'workshop' no 'INSTALLED_APPS' do projeto:

    # encoinfo/settings.py
    INSTALLED_APPS = [
        # apps instalados por padrão

        'workshop',
    ]

Execute as migrações dos apps instalados por padrão:

    # console
    $ python manage.py makemigrations showmigrations
    $ python manage.py makemigrations migrate

Crie uma migração para o app 'workshop':

    # console
    $ python manage.py makemigrations workshop
    $ python manage.py showmigrations workshop
    $ python manage.py migrate

Agora precisamos representar os inscritos através de um model. Para isso, crie o model 'Participante' no arquivo 'models.py':

    # workshop/models.py
    class Participante(models.Model):
        nome = models.CharField(u'Nome', max_length=200)
        idade = models.IntegerField(u'Idade', null=True, blank=True)
        cpf = models.IntegerField(u'CPF', unique=True)
        workshops = models.ManyToManyField(Workshop, related_name='participantes')

        def __unicode__(self):
            return u'{}'.format(self.nome)

Crie uma migração para o app 'workshop':

    # console
    $ python manage.py makemigrations workshop
    $ python manage.py showmigrations workshop
    $ python manage.py migrate

## Configurando o admin do django

Crie um usuário para o admin chamado 'admin' com a senha 'admin':

    # console
    $ python manage.py createsuperuser

Note que foram utilizados os validadores de senha definidos 'AUTH_PASSWORD_VALIDATORS', definidos no arquivo 'settings'. Agora crie o usuário 'admin' com a senha 'rootroot'.

Dentro do app workshop, no arquivo 'workshop/admin.py', registre o model 'Workshop'.

    # workshop/models.py
    from django.contrib import admin

    from models import Workshop

    admin.site.register(Workshop)

Vamos criar alguns workshops.

Talvez seria melhor ter uma descrição do workshop para o público entender o que será abordado. Pra isso, precisamos alterar o arquivo 'workshop/models.py' para adicionar um campo. Como sabemos que tipo de campo adicionar? Consultamos a documentação  com a [referência de fields do model](https://docs.djangoproject.com/en/1.9/ref/models/fields/). Após a consulta, verificamos que o tipo adequado para a descrição é o 'models.TextField'.

    # workshop/models.py

    from __future__ import unicode_literals

    from django.db import models


    class Workshop(models.Model):
        nome = models.CharField(u'Nome', max_length=200)
        slug = models.SlugField(u'Slug', max_length=200)
        vagas = models.IntegerField(u'Quantidade de vagas')
        # campo adicionado
        descricao = models.TextField(u'Descrição', null=True, blank=True)

        def __unicode__(self):
            return '{}'.format(self.nome)

Agora criamos uma migração para o app 'workshop':

    # console
    $ python manage.py showmigrations workshop
    $ python manage.py makemigrations workshop
    $ python manage.py showmigrations workshop
    $ python manage.py migrate

Precisamos criar um model que represente um inscrito no curso. Sendo assim, em 'workshop/models.py', adicionamos a classe:

    # imports

    # class Workshop(models.Model):

    class Participante(models.Model):
        nome = models.CharField(u'Nome', max_length=200)
        idade = models.IntegerField(u'Idade', null=True, blank=True)
        cpf = models.IntegerField(u'CPF', unique=True)
        workshops = models.ManyToManyField(Workshop, blank=True, related_name='participantes')

        def __unicode__(self):
            return u'{}'.format(self.nome)

Agora criamos uma migração para o app 'workshop':

    # console
    $ python manage.py showmigrations workshop
    $ python manage.py makemigrations workshop
    $ python manage.py sqlmigrate core 0000
    $ python manage.py showmigrations workshop
    $ python manage.py migrate

Qual o próximo passo? Registrar o model Participante no admin.

    # workshop/admin.py
    from django.contrib import admin

    from models import Workshop, Participante

    admin.site.register(Workshop)
    admin.site.register(Participante)

E agora? Adicionamos alguns participantes nos workshops.

Em seguida, vamos personalizar o admin para adicionar alguns filtros:

    # workshop/admin.py
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


## Exercícios
* é interessante que os inscritos tenham um e-mail para a organização do evento entrar em contato com eles caso necessário. Adicione o campo 'email' no model 'Participante' (lembre de usar os tipos de campos adequados);
* crie uma home pro site do encoinfo;
