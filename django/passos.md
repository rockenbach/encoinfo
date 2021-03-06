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

O que falta pra entregarmos isso e recebermos nosso dinheiro? Talvez a validação para evitar que o curso tenha mais inscritos do que a quantidade de vagas. Pra isso, veremos o conceito de forms.

### Django forms

De uma forma simples, os forms do django são estruturas que podem, dentre outras possibilidades, gerar automaticamente formulários que representem models existentes para que o usuário possa manipular os dados do sistema. Os forms não são usados apenas no admin do django, como veremos durante o curso, eles também são utilizados nos templates para gerar páginas customizadas. Todos os detalhes sobre os forms podem ser consultados na [documentação oficial](https://docs.djangoproject.com/en/1.9/topics/forms/).

Os formulários django são armazenados no arquivo 'forms.py' existente dentro de cada app. Vamos adicionar no arquivo 'workshop/forms.py' dois forms: um para representar o model Workshop e outro pra representar o model 'Participante':

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

Como esses models possuem validações diferentes do padrão, temos que falar pro admin do django utilizar eles ao invés do form padrão. Para isso, temos que alterar o arquivo 'workshop/admin.py':

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

Agora podemos fazer os testes no admin e ver a mágica acontecendo. Já que tudo está funcionando, podemos entregar o sistema e ganhar nossa grana.

# Adicionando a interface pública

A nossa cliente solicitou uma interface pública para listar todos os workshops e os inscritos em cada curso. Como ela está pagando, vamos desenvolver.

A partir de agora, os arquivos mencionados no tutorial devem ser consultados no [repositório do Github](https://github.com/rockenbach/encoinfo/tree/master/django).

Para isso, iremos utilizar o conceito as 'class-based views' nas nossas views e não as 'function-based views' como vimos ontem.

Uma view é uma estrutura que recebe uma requisição e retorna uma resposta. Nas 'function-based views' toda url redireciona para uma função, como, por exemplo 'def index(request)', que irá retornar uma resposta específica para uma entrada informada pelo usuário. Nas 'class-based views' toda url redireciona para uma instância de uma classe, que executará uma sequência de funções e também retornará um resultado. Para saber mais sobre as 'class-based views', consulte a [documentação oficial](https://docs.djangoproject.com/en/1.9/topics/class-based-views/) e o site [https://ccbv.co.uk/](https://ccbv.co.uk/).

Vamos começar pela listagem de workshops. No arquivo 'workshop/views.py' iremos criar uma classe que herdará de django.views.generic.ListView. Essa classe tem como objetivo retornar a lista de registros existentes no banco de dados referentes a um model específico. Nosso exemplo terá as seguintes propriedades:

* model: indica qual o model que deve ter os dados listados
* template_name: indica qual o arquivo de template será usado para renderizar o que o usuário visualiza
* context_object_name: indica qual o nome da variável que contém a lista de workshops para serem exibidos no template

Crie o template 'templates/lista.html'. Nesse template temos a estrutura de repetição '{% for workshop in workshops %}' que irá iterar sobre a lista de workshops cadastrados, armazenados na variável 'workshops'.

O próximo passo é adicionar a url pública que será acessada. Para isso, temos que alterar os arquivos 'encoinfo/urls.py' e 'workshop/urls.py'.

Alterações em 'encoinfo/urls.py':

    # importamos o include
    from django.conf.urls import include, url
    from django.contrib import admin

    urlpatterns = [
        url(r'^admin/', admin.site.urls),
        # definimos que a url 'workshops' incluirá todas as urls do app 'workshop'
        url(r'^workshops/', include('workshop.urls', namespace='workshop')),
    ]

Alterações em 'workshop/urls.py':

    from django.conf.urls import url

    from views import WorkshopList

    urlpatterns = [
        url(r'^$', WorkshopList.as_view(), name='lista')
    ]

Pronto, temos uma lista pública usável. Agora temos que mostrar a lista de todos os inscritos em cada workshop.

Para isso, iremos criar uma outra classe em 'workshop/views.py', porém, essa classe herdará de django.views.generic.DetailView. Essa classe tem como objetivo mostrar os detalhes de determinado registro existente no banco de dados. No nosso exemplo, a classe criada terá as mesmas propriedades do exemplo anterior: model, template_name e context_object_name.

Crie o template 'templates/detalhe.html'. Nesse template temos a estrutura de repetição '{% for participante in workshop.participantes.all %}' que irá iterar sobre a lista de participantes inscritos, armazenados na queryset participantes, definida no model Participante como related_name 'participantes'.

A única alteração de urls deverá ser feita no arquivo 'workshop/urls.py':

    from django.conf.urls import url

    from views import WorkshopList, WorkshopDetail

    urlpatterns = [
        url(r'^$', WorkshopList.as_view(), name='lista'),
        url(r'^detalhe/(?P<slug>[\w-]+)/$', WorkshopDetail.as_view(), name='detalhe')
    ]

Com isso, terminamos nosso minicurso. Dúvidas?

# Exercícios
* é interessante que os inscritos tenham um e-mail para a organização do evento entrar em contato com eles caso necessário. Adicione o campo 'email' no model 'Participante' (lembre de usar os tipos de campos adequados);
* crie uma home pro site do encoinfo;

# Referências adicionais

* [models e databases](https://docs.djangoproject.com/en/1.9/topics/db/)
* [url dispatcher](https://docs.djangoproject.com/en/1.9/topics/http/urls/)
* [templates](https://docs.djangoproject.com/en/1.9/topics/templates/)
* [built-in template tags and filters](https://docs.djangoproject.com/en/1.9/ref/templates/builtins/)
* [forms](https://docs.djangoproject.com/en/1.9/topics/forms/)
* [documentação oficial](https://docs.djangoproject.com/en/1.9/)
