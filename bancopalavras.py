class Banco(object):
    def __init__(self,palavras,dificuldade):
        self.ordem = palavras
        if dificuldade==1:
            self.frase = 'SUJEITO + VERBO + PREDICATIVO'
        elif dificuldade==2:
            self.frase = 'SUJEITO + VERBO TRANSITIVO + OBJETO'
        elif dificuldade==3:
            self.frase = 'SUJEITO + VERBO INTRANSITIVO + ADJUNTO ADVERBIAL'
        elif dificuldade==4:
            self.frase = 'SUJEITO PACIENTE + LOCUÇÃO VERBAL + AGENTE DA PASSIVA'

def bancodeFases(dificuldade):
    vetor = []
    if dificuldade==1:
        vetor.append(Banco(['a moça','chegou','bonita'],dificuldade))
        vetor.append(Banco(['o senhor','parece', 'cansado'], dificuldade))
        vetor.append(Banco(['ele','acordou', 'alegre'], dificuldade))
        vetor.append(Banco(['a comida', 'está', 'pronta'], dificuldade))
        vetor.append(Banco(['nós', 'vivemos', 'juntos'], dificuldade))
        vetor.append(Banco(['eu', 'estive', 'doente'], dificuldade))
        vetor.append(Banco(['ela', 'está', 'machucada'], dificuldade))
        vetor.append(Banco(['eu', 'passei', 'mal'], dificuldade))
        vetor.append(Banco(['eu', 'estou', 'chocado'], dificuldade))
        vetor.append(Banco(['nós', 'vivemos', 'correndo'], dificuldade))
        vetor.append(Banco(['jõao', 'passa', 'bem'], dificuldade))
        vetor.append(Banco(['gato', 'está', 'brincando'], dificuldade))
        vetor.append(Banco(['ele', 'está', 'lindo'], dificuldade))
    elif dificuldade==2:
        vetor.append(Banco(['eu', 'gosto', 'de você'], dificuldade))
        vetor.append(Banco(['ela', 'ama', 'bolo'], dificuldade))
        vetor.append(Banco(['a senhora', 'pegou', 'as cartas'], dificuldade))
        vetor.append(Banco(['o cavalo', 'mordeu', 'a cenoura'], dificuldade))
        vetor.append(Banco(['o dj', 'tocou', 'a música'], dificuldade))
        vetor.append(Banco(['a festa', 'precisava', 'de um palhaço'], dificuldade))
        vetor.append(Banco(['nós', 'fizemos', 'bolo'], dificuldade))
        vetor.append(Banco(['o ônibus', 'atropelou', 'a moça'], dificuldade))
        vetor.append(Banco(['ana', 'comprou', 'chocolates'], dificuldade))
        vetor.append(Banco(['ela', 'comprou', 'bolsas'], dificuldade))
        vetor.append(Banco(['joão', 'precisa', 'de meias'], dificuldade))
        vetor.append(Banco(['a vaca', 'ama', 'capim'], dificuldade))
        vetor.append(Banco(['eu', 'comi', 'sushi'], dificuldade))

    elif dificuldade==3:
        vetor.append(Banco(['a senhora','morreu','ontem'],dificuldade))
        vetor.append(Banco(['eu', 'cheguei', 'em casa'], dificuldade))
        vetor.append(Banco(['a jovem', 'correu', 'muito'], dificuldade))
        vetor.append(Banco(['ela', 'nasceu', 'na semana passada'], dificuldade))
        vetor.append(Banco(['o bebê', 'caiu', 'da cama'], dificuldade))
        vetor.append(Banco(['minha filha', 'casou', 'em paris'], dificuldade))
        vetor.append(Banco(['a criança', 'brincou', 'a tarde toda'], dificuldade))
        vetor.append(Banco(['nós', 'erramos', 'durante o jogo'], dificuldade))
        vetor.append(Banco(['o cão', 'levantou', 'lentamente'], dificuldade))
        vetor.append(Banco(['ele', 'escorregou', 'no piso'], dificuldade))
        vetor.append(Banco(['o gato', 'miava', 'todo dia'], dificuldade))
        vetor.append(Banco(['o time', 'errou', 'nas transações'], dificuldade))
        vetor.append(Banco(['os cães', 'brincam', 'sozinhos'], dificuldade))

    elif dificuldade==4:
        vetor.append(Banco(['a comida', 'foi feita', 'pelo pai'], dificuldade))
        vetor.append(Banco(['a casa', 'foi vendida', 'pelo jovem'], dificuldade))
        vetor.append(Banco(['o relatório', 'foi impresso', 'pela menina'], dificuldade))
        vetor.append(Banco(['o carro', 'foi lavado', 'pelo pai'], dificuldade))
        vetor.append(Banco(['o quadro', 'foi pintado', 'pelo jovem'], dificuldade))
        vetor.append(Banco(['as cartas', 'são escritas', 'por mim'], dificuldade))
        vetor.append(Banco(['a escola', 'será reformada', 'pela prefeitura'], dificuldade))
        vetor.append(Banco(['natais', 'são marcados', 'pela família'], dificuldade))
        vetor.append(Banco(['a viagem', 'será paga', 'pela empresa'], dificuldade))
        vetor.append(Banco(['a tv', 'será comprada', 'por mim'], dificuldade))
        vetor.append(Banco(['a bicicleta', 'foi comprada', 'pelo meu pai'], dificuldade))
        vetor.append(Banco(['as partidas', 'são apitadas', 'por arbítros'], dificuldade))
        vetor.append(Banco(['os jogadores', 'são pagos', 'pela liga'], dificuldade))
        vetor.append(Banco(['as propagandas', 'são criadas', 'pela empresa'], dificuldade))
        vetor.append(Banco(['o armário', 'é produzido', 'por madeireiras'], dificuldade))
        vetor.append(Banco(['os sapatos', 'são produzidos', 'pela china'], dificuldade))
        vetor.append(Banco(['o computador', 'é desenvolvido', 'pela dell'], dificuldade))
        vetor.append(Banco(['as palestras', 'foram organizadas', 'pela escola'], dificuldade))
        vetor.append(Banco(['o treinador', 'foi dispensado', 'pelo clube'], dificuldade))
        vetor.append(Banco(['o ps5', 'será lançado', 'pela sony'], dificuldade))
        vetor.append(Banco(['o carro', 'foi comprado', 'pela firma'], dificuldade))
        vetor.append(Banco(['a aula', 'foi ministrada', 'pelo aluno'], dificuldade))
        vetor.append(Banco(['a casa', 'foi construida', 'pelo meu primo'], dificuldade))
        vetor.append(Banco(['o quadro', 'será vendido', 'pelo dono'], dificuldade))
        vetor.append(Banco(['a praia', 'foi visitada', 'por ela'], dificuldade))
        vetor.append(Banco(['o lanche', 'será comprado', 'por mim'], dificuldade))

    return vetor
