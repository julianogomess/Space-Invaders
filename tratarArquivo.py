
arquivoscore = 'score.txt'
class Score(object):
    def __init__(self, nome, pontos):
        self.nome = nome
        self.pontos = int(pontos)

    def get_pontos(self):
        return self.pontos

    def get_nome(self):
        return self.nome

def colocaMaisculo(l):
    for x in range(l.__len__()):
        l[x] = l[x].upper()
    return l


def remove_repetidos(l):
    lista = l
    i = 0
    while i < len(lista):
        j = i + 1
        while j < len(lista):
            if lista[j] == lista[i]:
                del(lista[j])
            else:
                j = j + 1
        i = i + 1
    return sorted(lista)



def lerScore():
    l = []
    arquivo = open(arquivoscore, 'r')
    l = arquivo.readlines()
    for x in range(len(l)):
        l[x] = l[x].rstrip("\n")
        nome = ''
        pontos = ''
        teste = False
        for c in l[x]:
            if c == ' ':
                teste = True
            else:
                if teste:
                    pontos += c
                else:
                    nome+=c
        obs = Score(nome,int(pontos))
        l[x] = obs
    arquivo.close()
    return l



def escreverScore(l):
    arquivo = open(arquivoscore,'w')
    for x in l:
        msg = x.get_nome() + ' ' + str(x.get_pontos()) + '\n'
        arquivo.write(msg)
    arquivo.close()

def verScore(novoNome,novoPonto):
    l = lerScore()
    x = l[l.__len__()-1].pontos
    if x > novoPonto:
        record = False
    else:
        record = True
    obs = Score(novoNome, novoPonto)
    l.append(obs)
    lo = sorted( l , key = Score.get_pontos,reverse=True)
    lo.pop()
    escreverScore(lo)
    return record

    



#verScore('junior', 9080)
