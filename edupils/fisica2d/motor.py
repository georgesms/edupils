from vetor import Vetor
import grandezas
from .. import desenho

class Simulacao:
    def __init__(
            self, 
            largura=500,
            altura=300,
            raio_max=50,
            pixels_por_metro=10,
            tempo_total=grandezas.Tempo(10),
            tempo_por_frame=grandezas.Tempo(.1),
            plotar_escala=True,
            plotar_trajetoria=False,
            plotar_velocidade=False,    
        ):
        self.largura = largura
        self.altura = altura
        self.raio_maximo = raio_max  # Define o tamanho de cada célula na grade
        self.objetos = []  # Lista para armazenar os objetos na simulação

        self.T = tempo_total
        self.dt = tempo_por_frame

    def adicionar_objeto(self, objeto):
        """Adiciona um novo objeto à simulação e o posiciona na grade espacial."""
        self.objetos.append(objeto)
    
    def ordenar_objetos(self):
        self.objetos = sorted(self.objetos, key=lambda ob: ob.x)

    def varredura_colisoes(self):
        self.ordenar_objetos()
        colisoes = []
        for i in range(len(self.objetos)-1):
            for j in range(i+1, len(self.objetos)):
                if self.detectar_colisao_entre_objetos(self.objetos[i], self.objetos[j]):
                    colisoes.append((i, j))
                
                if ((self.objetos[i].x + self.raio_maximo) < 
                    (self.objetos[j].x - self.raio_maximo)):
                    break

    def detectar_colisao_entre_objetos(self, objeto1, objeto2):
        """Verifica se há colisão entre dois objetos."""
        dx = objeto1.x - objeto2.x
        dy = objeto1.y - objeto2.y
        distancia = (dx**2 + dy**2)**0.5
        return distancia < (objeto1.raio + objeto2.raio)


    def vetor_normal_a_colisao(self, objeto1, objeto2):
        """Calcula o vetor normal à colisão entre dois objetos.
            Devolve os componentes x e y do vetor normal e a distância entre os objetos.
        """
        dx = objeto1.x - objeto2.x
        dy = objeto1.y - objeto2.y
        distancia = (dx**2 + dy**2)**0.5
        return dx / distancia, dy / distancia, distancia

    def resolver_colisao(self, objeto1, objeto2):
        """Resolve a colisão ajustando as posições e velocidades dos objetos."""
        
        normal_x, normal_y, distancia = self.vetor_normal_a_colisao(objeto1, objeto2)

        # Calcular o mínimo de deslocamento necessário
        deslocamento = (objeto1.raio + objeto2.raio - distancia) / 2

        # Ajustar posições
        objeto1.x += normal_x * deslocamento
        objeto1.y += normal_y * deslocamento
        objeto2.x -= normal_x * deslocamento
        objeto2.y -= normal_y * deslocamento

        tangente_x = -normal_y
        tangente_y = normal_x

    def atualizar_estado(self):
        """Atualiza o estado da simulação."""
        self.aplicar_forcas()
        self.detectar_e_resolver_colisoes()
        for objeto in self.objetos:
            objeto.atualiza_estado(self.dt)

class Forca(Vetor):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Objeto:
    def __init__(self, x, y, vx, vy, massa=1):
        self.posicao = Vetor(
            grandezas.Posicao(x), 
            grandezas.Posicao(y)
        )
    
        self.velocidade = Vetor(
            grandezas.Velocidade(vx), 
            grandezas.Velocidade(vy)
        )
        self.massa = grandezas.Massa(massa)
        self.forcas = []

    def adiciona_forca(self, forca):
        self.forcas.append(forca)
    
    def aceleração_resultante(self):
        ax = sum(forca.x for forca in self.forcas) / self.massa
        ay = sum(forca.y for forca in self.forcas) / self.massa
        return ax, ay

    def atualiza_estado(self, dt):
        ax, ay = self.aceleracao_resultante()
        self.vx += ax * dt
        self.vy += ay * dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        # Resetar as forcas após a atualização
        self.forcas = []

class Círculo(Objeto):
    def __init__(self, x, y, vx, vy, raio, massa, cor="roxo"):
        if massa is None:
            massa = raio ** 2
        super().__init__(x, y, vx, vy, massa)
        self.raio = raio

    def centro(self):
        return self.x, self.y
    
    def plotar(self, canvas_id):
        desenho.desenhar_arco(
            self.x, 
            self.y, 
            self.raio, 
            0, 
            2 * math.pi, 
            canvas_id, 
            self.cor
        )
    
if __name__ == "__main__":
    sim = Simulacao(
        largura=500,
        altura=300,
        raio_max=50,
        pixels_por_metro=10,
        tempo_total=grandezas.Tempo(10),
        tempo_por_frame=grandezas.Tempo(.1),
        plotar_escala=True,
        plotar_trajetoria=True,
        plotar_velocidade=True,
    )

    cir = 
