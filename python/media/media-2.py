# coding: utf-8


def verifica_media():
    try:
        media = int(input('informe a media: '))

        if media <= 2:
            print 'se lascou, cara'
        elif media > 2 and media < 4:
            print 'faça a recuperação'
        else:
            print 'passou, "miserávi"!!!'

        return media
    except ValueError:
        print 'ERRO: o valor informado não é um número'

media = verifica_media()

if media is not None:
    print 'a média informada foi: %d' % (media)
