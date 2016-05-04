# coding: utf-8

try:
    media = input('informe a media: ')

    if media <= 2:
        print 'se lascou, cara'
    elif media > 2 and media < 4:
        print 'faça a recuperação'
    else:
        print 'passou, "miserávi"!!!'

except ValueError:
    print 'ERRO: O valor informado não é um número'
