import random
from abc import ABC, abstractmethod

class Labirinto:
    DIRECOES = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    PAREDE = '@'
    CELULA = '_'
    NAO_VISITADO = '.'

    def __init__(self, altura, largura):
        self.altura = altura
        self.largura = largura
        self.labirinto = [[Labirinto.NAO_VISITADO for _ in range(largura)] for _ in range(altura)]
        self.paredes = []
        
        self.entrada = None
        self.saida = None

        self._gerar_labirinto()
        self._processamento_pos_geracao()

        self.representacao = None

    def _contar_celulas_adjacentes(self, parede_aleatoria, tipo_posicao):
        celulas_adjacentes = 0
        h, w = parede_aleatoria
        for dH, dW in Labirinto.DIRECOES:
            if self.labirinto[h+dH][w+dW] == tipo_posicao:
                celulas_adjacentes += 1
        return celulas_adjacentes

    def _gerar_posicao_no_meio(self):
        h = int(random.random() * (self.altura - 2)) + 1
        w = int(random.random() * (self.largura - 2)) + 1
        return h, w

    def _gerar_labirinto(self):
        altura_inicial, largura_inicial = self._gerar_posicao_no_meio()
        self.labirinto[altura_inicial][largura_inicial] = Labirinto.CELULA
        for dH, dW in Labirinto.DIRECOES:
            self.paredes.append([altura_inicial + dH, largura_inicial + dW])
            self.labirinto[altura_inicial + dH][largura_inicial + dW] = Labirinto.PAREDE

        while self.paredes:
            parede_aleatoria = self.paredes[int(random.random()*len(self.paredes))-1]

            for h, w in Labirinto.DIRECOES:
                direcao_encontrada = False
                if 0 < parede_aleatoria[0] < self.altura-1 and 0 < parede_aleatoria[1] < self.largura-1:
                    if self.labirinto[parede_aleatoria[0]+h][parede_aleatoria[1]+w] == Labirinto.NAO_VISITADO and self.labirinto[parede_aleatoria[0]-h][parede_aleatoria[1]-w] == Labirinto.CELULA:
                        direcao_encontrada = True
                        celulas_adjacentes = self._contar_celulas_adjacentes(parede_aleatoria, Labirinto.CELULA)
                        if celulas_adjacentes < 2:
                            self.labirinto[parede_aleatoria[0]][parede_aleatoria[1]] = Labirinto.CELULA
                            for h2, w2 in Labirinto.DIRECOES:
                                if (h2, w2) != (-h, -w):
                                    if self.labirinto[parede_aleatoria[0]+h2][parede_aleatoria[1]+w2] != Labirinto.CELULA:
                                        self.labirinto[parede_aleatoria[0]+h2][parede_aleatoria[1]+w2] = Labirinto.PAREDE
                                    if [parede_aleatoria[0]+h2, parede_aleatoria[1]+w2] not in self.paredes:
                                        self.paredes.append([parede_aleatoria[0]+h2, parede_aleatoria[1]+w2])
                        if parede_aleatoria in self.paredes:
                            self.paredes.remove(parede_aleatoria)

                if direcao_encontrada:
                    break

            if parede_aleatoria in self.paredes:
                self.paredes.remove(parede_aleatoria)

    def _processamento_pos_geracao(self):
        # Transformar células não visitadas em paredes
        for i in range(self.altura):
            for j in range(self.largura):
                if self.labirinto[i][j] == Labirinto.NAO_VISITADO:
                    self.labirinto[i][j] = Labirinto.PAREDE

        # Definir entrada e saída
        for i in range(self.largura):
            if self.labirinto[1][i] == Labirinto.CELULA:
                self.labirinto[0][i] = Labirinto.CELULA
                self.entrada = (0, i)
                break

        for i in range(self.largura-1, 0, -1):
            if self.labirinto[self.altura-2][i] == Labirinto.CELULA:
                self.labirinto[self.altura-1][i] = Labirinto.CELULA
                self.saida = (self.altura-1, i)
                break

    def mostrar_labirinto(self):
        for linha in self.labirinto:
            print(' '.join(linha))


    def eh_parede(self, coordenada):
        h, w = coordenada
        return self.labirinto[h][w] == Labirinto.PAREDE
    

class Jogador(ABC):
    DIRECOES = {
        'norte': (-1, 0),
        'sul': (1, 0),
        'leste': (0, 1),
        'oeste': (0, -1)
    }
    DIRECORES_INV = {v:k for k,v in DIRECOES.items()}

    def __init__(self, labirinto):
        self.labirinto = labirinto
        self.posicao = labirinto.entrada

    @abstractmethod
    def mover(self):
        pass

    def mostrar_jogador_e_labirinto(self):
        for i, linha in enumerate(self.labirinto.labirinto):
            for j, celula in enumerate(linha):
                if (i, j) == self.posicao:
                    print(self.representacao, end=' ')
                else:
                    print(celula, end=' ')
            print()


class JogadorComBussola(Jogador):

    def __init__(self, labirinto):
        super().__init__(labirinto)
        self.representacao = "X"

    def mover(self, direcao):
        if direcao in JogadorComBussola.DIRECOES:
            dH, dW = JogadorComBussola.DIRECOES[direcao]
            nova_posicao = (self.posicao[0] + dH, self.posicao[1] + dW)

            if not self.labirinto.eh_parede(nova_posicao):
                self.posicao = nova_posicao
                return True
        return False


class JogadorOrientado(Jogador):
    OPCOES_REPRESENTACAO = {
        'norte': '^',
        'leste': '>',
        'sul': 'v',
        'oeste': '<'
    }

    def __init__(self, labirinto):
        super().__init__(labirinto)
        self.orientacao = "sul"
        self.vetor = Jogador.DIRECOES[self.orientacao]
        self.representacao = JogadorOrientado.OPCOES_REPRESENTACAO[self.orientacao]

    def virar(self, direcao):
        h, w = self.vetor
        if direcao == 'esquerda':
            self.vetor = (-w, h)
            
        elif direcao == 'direita':
            self.vetor = (w, -h)

        self.orientacao = Jogador.DIRECORES_INV[self.vetor]
        self.representacao = JogadorOrientado.OPCOES_REPRESENTACAO[self.orientacao]
        
    def mover(self):
        dH, dW = self.vetor
        nova_posicao = (self.posicao[0] + dH, self.posicao[1] + dW)

        if not self.labirinto.eh_parede(nova_posicao):
            self.posicao = nova_posicao
            return True
        return False