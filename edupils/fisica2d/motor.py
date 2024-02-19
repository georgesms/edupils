class Força:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Objeto:
    def __init__(self, x, y, theta, vx, vy, massa):
        self.x = x
        self.y = y
        self.theta = theta
        self.vx = vx
        self.vy = vy
        self.massa = massa
        self.forças = []

    def adiciona_força(self, força):
        self.forças.append(força)
    
    def aceleração_resultante(self):
        ax = sum(força.x for força in self.forças) / self.massa
        ay = sum(força.y for força in self.forças) / self.massa
        return ax, ay

    def atualiza_estado(self, dt):
        ax, ay = self.aceleração_resultante()
        self.vx += ax * dt
        self.vy += ay * dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        # Resetar as forças após a atualização
        self.forças = []

class Círculo(Objeto):
    def __init__(self, x, y, theta, vx, vy, massa, raio):
        super().__init__(x, y, theta, vx, vy, massa)
        self.raio = raio

    def detecção_de_colisão(self):
        pass  # Implementar lógica de detecção de colisão

    def baricentro(self):
        return self.x, self.y

class Retângulo(Objeto):
    def __init__(self, x, y, theta, vx, vy, massa, largura, altura):
        super().__init__(x, y, theta, vx, vy, massa)
        self.largura = largura
        self.altura = altura

    def detecção_de_colisão(self):
        pass  # Implementar lógica de detecção de colisão

    def baricentro(self):
        return self.x + self.largura / 2, self.y + self.altura / 2

class Polyline(Objeto):
    def __init__(self, x, y, theta, vx, vy, massa, pontos):
        super().__init__(x, y, theta, vx, vy, massa)
        self.pontos = pontos  # Lista de tuplas (x, y) representando os vértices

    def detecção_de_colisão(self):
        pass  # Implementar lógica de detecção de colisão

    def baricentro(self):
        pass  # Implementar cálculo de baricentro
