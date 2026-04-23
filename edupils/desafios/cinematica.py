from edupils import constantes, desenho
import asyncio


def _normalizar_posicao(posicao):
    """Aceita escalar ou par (x, y); devolve sempre (x, y)."""
    if isinstance(posicao, (tuple, list)):
        return (float(posicao[0]), float(posicao[1]))
    return (float(posicao), 0.0)


class Objeto:
    def __init__(
        self,
        nome,
        posicao_inicial,
        funcao_movimento=None,
        forma="quadrado",
        cor="azul",
        origem_em_metros=(10, 1),
        pixels_por_metro=25,
        rastro=False,
    ):
        self.nome = nome
        self.posicao = _normalizar_posicao(posicao_inicial)
        self.funcao_movimento = funcao_movimento or (lambda t: self.posicao)
        self.forma = forma
        self.cor = cor
        self.origem_metros = origem_em_metros
        self.pixels_por_metro = pixels_por_metro
        self.rastro = rastro
        self.desenhar()

    def desenhar(self, camada=constantes.NOME_PAINEL_FRENTE):
        ox, oy = self.origem_metros
        ppm = self.pixels_por_metro
        x_m, y_m = self.posicao
        x = (x_m + ox) * ppm
        # y cresce para cima no mundo; na tela cresce para baixo.
        # O -1 mantém o sprite logo acima do eixo x quando y=0 (preserva o visual 1D).
        y = (oy - 1 - y_m) * ppm
        if self.forma == "quadrado":
            desenho.desenhar_retangulo(
                x, y, 20, 20, camada, cor_preenchimento=self.cor
            )
        elif self.forma == "triangulo":
            desenho.desenhar_triangulo(
                x + 10, y + 12, 14, self.cor, camada, angulo=90, proporcao_base=1.61
            )
        elif self.forma == "circulo":
            desenho.desenhar_arco(
                x + 10, y + 10, 10, 0, 360, camada,
                cor_preenchimento=self.cor, cor_contorno=self.cor, largura_contorno=1,
            )


class Animacao:
    def __init__(
        self,
        tempo=10,
        frames_por_segundo=10,
        distancia_em_metros=20,
        origem_em_metros=(10, 1),
        pixels_por_metro=25,
    ):
        self.tempo = tempo
        self.frames_por_segundo = frames_por_segundo
        if isinstance(distancia_em_metros, (tuple, list)):
            self.distancia_em_metros = (int(distancia_em_metros[0]), int(distancia_em_metros[1]))
        else:
            self.distancia_em_metros = (int(distancia_em_metros), int(distancia_em_metros))
        self.origem_em_metros = origem_em_metros
        self.pixels_por_metro = pixels_por_metro
        self.objetos = {}
        self.desenhar_eixos()

    def adicionar_objeto(
        self,
        nome,
        posicao_inicial,
        funcao_movimento,
        forma="quadrado",
        cor="azul",
        rastro=False,
    ):
        self.objetos[nome] = Objeto(
            nome,
            posicao_inicial,
            funcao_movimento,
            forma=forma,
            cor=cor,
            origem_em_metros=self.origem_em_metros,
            pixels_por_metro=self.pixels_por_metro,
            rastro=rastro,
        )

    def desenhar_eixos(self, camada=constantes.NOME_PAINEL_AUXILIAR):
        desenho.apagar_painel(camada)
        ox, oy = self.origem_em_metros
        ppm = self.pixels_por_metro
        dx, dy = self.distancia_em_metros

        # --- eixo x (horizontal) ---
        y_eixo = oy * ppm
        desenho.desenhar_linha(
            (ox - dx) * ppm * 2, y_eixo,
            (ox + dx) * ppm * 2, y_eixo,
            id_canvas=camada,
        )
        for i in range(-2 * dx, 2 * dx + 1):
            x = (i + ox) * ppm
            desenho.escrever_texto(str(i), x + 2, y_eixo + 12, id_canvas=camada, tamanho=10)
            desenho.desenhar_linha(x, y_eixo, x, y_eixo + 5, id_canvas=camada)

        # --- eixo y (vertical) ---
        x_eixo = ox * ppm
        desenho.desenhar_linha(
            x_eixo, (oy - dy) * ppm * 2,
            x_eixo, (oy + dy) * ppm * 2,
            id_canvas=camada,
        )
        for j in range(-2 * dy, 2 * dy + 1):
            if j == 0:
                continue  # o "0" já foi escrito pelo eixo x
            y = (oy - j) * ppm
            desenho.escrever_texto(str(j), x_eixo + 4, y + 4, id_canvas=camada, tamanho=10)
            desenho.desenhar_linha(x_eixo, y, x_eixo - 5, y, id_canvas=camada)

    def desenhar_tempo(self, t, camada=constantes.NOME_PAINEL_FRENTE):
        desenho.escrever_texto(
            f"t = {t:.2f} s",
            400,
            100,
            id_canvas=camada,
            tamanho=12,
            cor="black",
        )

    def desenhar_quadro(self, t, camada=constantes.NOME_PAINEL_FRENTE):
        desenho.apagar_painel(camada)
        self.desenhar_tempo(t, camada=camada)
        for obj in self.objetos.values():
            obj.posicao = _normalizar_posicao(obj.funcao_movimento(t))
            obj.desenhar(camada=camada)

    def desenhar_rastro(self, t, camada=constantes.NOME_PAINEL_FUNDO):
        objetos_com_rastro = [obj for obj in self.objetos.values() if obj.rastro]
        if not objetos_com_rastro:
            return
        for obj in objetos_com_rastro:
            obj.posicao = _normalizar_posicao(obj.funcao_movimento(t))
            obj.desenhar(camada=camada)
        desenho.clarear_com_marca_dagua(camada, .6)

    def apagar_tudo(self):
        for camada in [constantes.NOME_PAINEL_FUNDO, constantes.NOME_PAINEL_FRENTE]:
            desenho.apagar_painel(camada)

    async def animar(self):
        self.apagar_tudo()
        max_steps = int(self.tempo * self.frames_por_segundo)
        dt = 1 / self.frames_por_segundo

        for step in range(max_steps):
            t = step * dt

            self.desenhar_quadro(t)
            if t % 1 < .001:
                self.desenhar_rastro(t)

            await asyncio.sleep(dt)