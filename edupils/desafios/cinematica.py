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

    def atualizar(self, t):
        self.posicao = _normalizar_posicao(self.funcao_movimento(t))

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


class Seta:
    def __init__(
        self,
        nome,
        origem,
        deslocamento,
        cor="vermelho",
        origem_em_metros=(10, 1),
        pixels_por_metro=25,
    ):
        self.nome = nome
        self.origem = origem                # função t -> (x, y) em metros
        self.deslocamento = deslocamento    # função t -> (dx, dy) em metros
        self.cor = cor
        self.origem_metros = origem_em_metros
        self.pixels_por_metro = pixels_por_metro
        self.rastro = False                 # setas não deixam rastro
        self.atualizar(0)
        self.desenhar()

    def atualizar(self, t):
        self.posicao = _normalizar_posicao(self.origem(t))
        self.vetor = _normalizar_posicao(self.deslocamento(t))

    def desenhar(self, camada=constantes.NOME_PAINEL_FRENTE):
        ox, oy = self.origem_metros
        ppm = self.pixels_por_metro
        x_m, y_m = self.posicao
        dx_m, dy_m = self.vetor
        x0 = (x_m + ox) * ppm
        y0 = (oy - y_m) * ppm            # seta usa coord. de mundo direta (sem o -1 do Objeto)
        dx_px = dx_m * ppm
        dy_px = -dy_m * ppm              # inverte y porque na tela cresce para baixo
        desenho.desenhar_seta(
            x0, y0, dx_px, dy_px,
            id_canvas=camada, cor=self.cor,
        )


class Grafico:
    CORES_PADRAO = ["roxo", "verde", "azul", "vermelho", "amarelo"]

    def __init__(
        self,
        curvas,
        eixo_y="",
        tempo_max=10,
        cores=None,
        largura=constantes.LARGURA_PADRAO_GRAFICO,
        altura=constantes.ALTURA_PADRAO_GRAFICO,
        margem=40,
        amostras=200,
        painel_fundo=constantes.NOME_PAINEL_GRAFICO_FUNDO,
        painel_frente=constantes.NOME_PAINEL_GRAFICO_FRENTE,
    ):
        self.curvas = curvas
        self.eixo_y = eixo_y
        self.tempo_max = tempo_max
        self.largura = largura
        self.altura = altura
        self.margem = margem
        self.painel_fundo = painel_fundo
        self.painel_frente = painel_frente
        self.t_atual = 0

        # cor por curva: prioriza o que o aluno passou; cai no palette padrão.
        self.cores = {}
        for i, nome in enumerate(curvas):
            if cores and nome in cores:
                self.cores[nome] = cores[nome]
            else:
                self.cores[nome] = Grafico.CORES_PADRAO[i % len(Grafico.CORES_PADRAO)]

        # Pré-amostragem: descobre min/max do eixo y e guarda os pontos para redesenho.
        self.ts = [tempo_max * i / (amostras - 1) for i in range(amostras)]
        self.amostras = {}
        todos_y = []
        for nome, f in curvas.items():
            ys = [f(t) for t in self.ts]
            self.amostras[nome] = ys
            todos_y.extend(ys)

        self.y_min = min(todos_y)
        self.y_max = max(todos_y)
        span = self.y_max - self.y_min
        if span == 0:
            span = 1
        # folga de 10% em cima e embaixo para a curva não colar no eixo
        self.y_min -= span * 0.1
        self.y_max += span * 0.1

        self._desenhar_fundo()

    def _t_para_px(self, t):
        faixa = self.largura - 2 * self.margem
        return self.margem + (t / self.tempo_max) * faixa

    def _y_para_px(self, y):
        faixa = self.altura - 2 * self.margem
        return (self.altura - self.margem) - ((y - self.y_min) / (self.y_max - self.y_min)) * faixa

    def _desenhar_fundo(self):
        desenho.apagar_painel(self.painel_fundo)

        x_esq = self.margem
        x_dir = self.largura - self.margem
        y_topo = self.margem
        y_base = self.altura - self.margem

        # eixos
        desenho.desenhar_linha(x_esq, y_base, x_dir, y_base, id_canvas=self.painel_fundo)
        desenho.desenhar_linha(x_esq, y_topo, x_esq, y_base, id_canvas=self.painel_fundo)

        # rótulos
        desenho.escrever_texto("t [s]", x_dir + 5, y_base + 4, id_canvas=self.painel_fundo, tamanho=10)
        desenho.escrever_texto(self.eixo_y, x_esq - 5, y_topo - 5, id_canvas=self.painel_fundo, tamanho=10)

        # ticks no eixo t
        for i in range(6):
            t = self.tempo_max * i / 5
            x = self._t_para_px(t)
            desenho.desenhar_linha(x, y_base, x, y_base + 4, id_canvas=self.painel_fundo)
            desenho.escrever_texto(f"{t:.1f}", x - 8, y_base + 14, id_canvas=self.painel_fundo, tamanho=10)

        # ticks no eixo y
        for i in range(5):
            y_val = self.y_min + (self.y_max - self.y_min) * i / 4
            y = self._y_para_px(y_val)
            desenho.desenhar_linha(x_esq - 4, y, x_esq, y, id_canvas=self.painel_fundo)
            desenho.escrever_texto(f"{y_val:.1f}", x_esq - 32, y + 3, id_canvas=self.painel_fundo, tamanho=10)

        # curvas
        for nome, ys in self.amostras.items():
            cor = self.cores[nome]
            for i in range(len(self.ts) - 1):
                desenho.desenhar_linha(
                    self._t_para_px(self.ts[i]),
                    self._y_para_px(ys[i]),
                    self._t_para_px(self.ts[i + 1]),
                    self._y_para_px(ys[i + 1]),
                    id_canvas=self.painel_fundo, cor=cor, largura=2,
                )

        # legenda
        for i, nome in enumerate(self.curvas):
            cor = self.cores[nome]
            y_leg = y_topo + 10 + i * 15
            desenho.desenhar_linha(
                x_dir - 80, y_leg, x_dir - 60, y_leg,
                id_canvas=self.painel_fundo, cor=cor, largura=2,
            )
            desenho.escrever_texto(
                nome, x_dir - 55, y_leg + 3,
                id_canvas=self.painel_fundo, tamanho=10,
            )

    def atualizar(self, t):
        self.t_atual = t

    def desenhar(self):
        desenho.apagar_painel(self.painel_frente)
        x = self._t_para_px(self.t_atual)
        # cursor vertical
        desenho.desenhar_linha(
            x, self.margem, x, self.altura - self.margem,
            id_canvas=self.painel_frente,
            cor="cinza", largura=1, padrao="tracejada",
        )
        # ponto sobre cada curva no tempo atual
        for nome, f in self.curvas.items():
            y = self._y_para_px(f(self.t_atual))
            desenho.desenhar_circulo(
                x, y, 4,
                id_canvas=self.painel_frente,
                cor_preenchimento=self.cores[nome],
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
        self.grafico = None
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

    def adicionar_seta(
        self,
        nome,
        origem,
        deslocamento,
        cor="vermelho",
    ):
        self.objetos[nome] = Seta(
            nome,
            origem,
            deslocamento,
            cor=cor,
            origem_em_metros=self.origem_em_metros,
            pixels_por_metro=self.pixels_por_metro,
        )

    def adicionar_grafico(self, curvas, eixo_y="", cores=None):
        self.grafico = Grafico(
            curvas=curvas,
            eixo_y=eixo_y,
            tempo_max=self.tempo,
            cores=cores,
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
            obj.atualizar(t)
            obj.desenhar(camada=camada)

    def desenhar_rastro(self, t, camada=constantes.NOME_PAINEL_FUNDO):
        objetos_com_rastro = [obj for obj in self.objetos.values() if obj.rastro]
        if not objetos_com_rastro:
            return
        for obj in objetos_com_rastro:
            obj.atualizar(t)
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
            if self.grafico is not None:
                self.grafico.atualizar(t)
                self.grafico.desenhar()

            await asyncio.sleep(dt)