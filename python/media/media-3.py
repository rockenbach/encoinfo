# coding: utf-8


class Avaliacao(object):
    def verifica_media(self):
        try:
            media = int(input('informe a media: '))

            if media <= 2:
                print 'se lascou, cara'
            elif media > 2 and media < 4:
                print 'faça a recuperação'
            else:
                for i in range(0, media):
                    print '%d. passou, "miserávi"!!!' % (i)

            return media
        except ValueError:
            print 'ERRO: O valor informado não é um número'

    def __init__(self):
        media = self.verifica_media()

        if media is not None:
            print 'a média informada foi: %d' % (media)

avaliacao = Avaliacao()
