# edupils

Biblioteca de utilitários educacionais em Python para ilustrar conteúdos de
programação, matemática e física em notebooks [Starboard](https://starboard.gg/)
rodando sobre [Pyodide](https://pyodide.org/). A API é em português e foi
pensada para estudantes do ensino médio.

- **Autor:** Georges Spyrides
- **Licença:** MIT
- **PyPI:** [`edupils`](https://pypi.org/project/edupils/)
- **Repositório:** [github.com/georgesms/edupils](https://github.com/georgesms/edupils)

## Instalação

No ambiente Pyodide/Starboard:

```python
import micropip
await micropip.install("edupils")
```

Ou em um ambiente Python tradicional (para os módulos que não dependem do
browser):

```bash
pip install edupils
```

> ⚠️ Boa parte dos módulos desenha sobre o `<canvas>` da página e depende de
> `from js import document`. Esses módulos **só funcionam dentro do Pyodide**
> (Starboard, JupyterLite etc.). Módulos puros de Python (`fisica.vetor`,
> `fisica.grandezas`, `desafios.bejeweled`) rodam em qualquer lugar.

## Estrutura dos pacotes

```
edupils/
├── constantes.py      # cores, dimensões padrão e tradução PT-EN
├── desenho/           # primitivas de desenho sobre <canvas> HTML
├── desafios/          # atividades prontas: tartaruga, labirinto, cinemática…
├── fisica/            # vetores, grandezas com unidades, simulação
├── imagem/            # placeholder para manipulação de imagens
└── sons/              # placeholder para áudio
```

### [edupils.constantes](edupils/constantes.py)

Dicionários de tradução (`"vermelho" → "red"`, `"tracejada" → "dashed"`),
cores-tema (`COR_PRIMARIA`, `COR_SECUNDARIA`) e dimensões padrão do canvas.
Todos os outros módulos consomem essas constantes para que o aluno possa
escrever em português natural.

### [edupils.desenho](edupils/desenho/)

Camada de desenho 2D sobre o `<canvas>`. Cria três painéis empilhados
(`painelFundo`, `painelAuxiliar`, `painelFrente`) para separar cenário,
trajetórias e atores.

Funções principais ([desenho.py](edupils/desenho/desenho.py)):

- `desenhar_retangulo(x, y, largura, altura, canvas_id, cor_preenchimento)`
- `desenhar_circulo(x, y, raio, id_canvas, cor_preenchimento, cor_contorno, largura_contorno)`
- `desenhar_arco(...)` — arco com ângulos em graus
- `desenhar_triangulo(x_baricentro, y_baricentro, raio_circunscrito, cor, id_canvas, angulo, proporcao_base)`
- `desenhar_linha(inicio_x, inicio_y, fim_x, fim_y, id_canvas, cor, largura, padrao)` — aceita `"solida"`, `"tracejada"`, `"pontilhada"`
- `escrever_texto(texto, x, y, id_canvas, cor, tamanho, fonte, alinhamento, direcao)`

Gerência de painéis ([painel.py](edupils/desenho/painel.py)):

- `criar_painel(largura, altura, …)` — monta a `<div>` com as três camadas
- `apagar_painel(id_painel)`
- `clarear_com_marca_dagua(id_painel, alpha)` — usado para criar rastros

### [edupils.desafios](edupils/desafios/)

Atividades completas prontas para usar em sala.

- **[tartaruga.py](edupils/desafios/tartaruga.py)** — uma *turtle graphics*
  simplificada. A tartaruga é desenhada como triângulo; há `andar`, `virar`,
  `abaixar_caneta` / `levantar_caneta`, `voltar_para_casa`, além de
  `mudar_cor_linha`, `mudar_padrao_linha` e `mudar_cor_tartaruga`.

  ```python
  from edupils.desafios.tartaruga import Tartaruga
  t = Tartaruga(cor_linha="roxo", padrao_linha="tracejada")
  t.abaixar_caneta()
  for _ in range(4):
      t.andar(80)
      t.virar(90)
  ```

- **[labirinto.py](edupils/desafios/labirinto.py)** — gerador procedural de
  labirintos (Prim randomizado) com entrada, saída bandeirada e um `Jogador`
  orientado que expõe `mover`, `virar("esquerda"/"direita")`,
  `redondezas_livres()` e `esta_livre(direcao)`. Ao chegar na saída, imprime
  “Parabéns!!”.

  ```python
  from edupils.desafios.labirinto import criar_labirinto_e_jogador
  lab, p = criar_labirinto_e_jogador()
  while not p.esta_livre("frente") and p.esta_livre("direita"):
      p.virar("direita")
  p.mover(3)
  ```

- **[cinematica.py](edupils/desafios/cinematica.py)** — animação 1D/2D do
  movimento de objetos, com eixos graduados, timestamp e rastro opcional
  por objeto. O aluno fornece uma `funcao_movimento(t)` — escalar para 1D,
  tupla `(x, y)` para 2D.

  ```python
  from edupils.desafios.cinematica import Animacao
  anim = Animacao(tempo=8, frames_por_segundo=20)
  # 1D
  anim.adicionar_objeto("bola", 0, lambda t: 2*t, cor="roxo", rastro=True)
  anim.adicionar_objeto("carro", 0, lambda t: 0.5*t**2, forma="triangulo", cor="verde")
  # 2D (lançamento oblíquo)
  anim.adicionar_objeto("projetil", (0, 0),
                        lambda t: (10*t, 20*t - 0.5*9.8*t**2),
                        cor="azul", rastro=True)
  await anim.animar()
  ```

- **[bejeweled.py](edupils/desafios/bejeweled.py)** — gera uma tabela aleatória
  de emojis (corações, quadrados, círculos em 4 cores) para exercícios de
  busca/combinação em grades. Puro Python + NumPy.

- **[p5.py](edupils/desafios/p5.py)** — cola mínima para usar a
  [p5.js](https://p5js.org/) a partir do Python no navegador.

### [edupils.fisica](edupils/fisica/)

Mini-engine física com ênfase em tipagem por grandeza.

- **[grandezas.py](edupils/fisica/grandezas.py)** — `Tempo`, `Posicao`,
  `Velocidade`, `Aceleracao`, `Massa`, `Forca`, `Energia` são subclasses de
  `float` com unidade e sobrecarga de operadores que respeita dimensões
  (`Velocidade * Tempo → Posicao`, `Forca / Massa → Aceleracao`, soma entre
  unidades diferentes levanta `TypeError`).
- **[vetor.py](edupils/fisica/vetor.py)** — `Vetor` 2D com `norma`,
  `normalizar`, `produto_escalar`, `projetar`, `perpendicular`, `aplicar(f)`
  e operadores `+ - * /`.
- **[forcas.py](edupils/fisica/forcas.py)** — `ForcaAtrito`, `ForcaElastica`,
  `ForcaGravitacao`, `ForcaEletromagnetica`, `ForcaArrasto` (todas herdam de
  `ForcaVetorial`).
- **[motor.py](edupils/fisica/motor.py)** — loop de simulação com objetos
  (`Objeto`, `Circulo`), integração de forças, detecção/resolução de colisões
  rígidas contra paredes e varredura de colisões entre objetos.

### [edupils.imagem](edupils/imagem/) e [edupils.sons](edupils/sons/)

Esqueleto para manipulação de imagens e áudio — ainda não implementados.

## TO-DO — extensões da `cinematica`

### Ordem sugerida

| Fase | Tarefa | Esforço | Destrava |
|------|--------|---------|----------|
| 1    | 1. Posição em 2D ✅                       | M | NB 08, 09, 10, 11, 13 |
| 2    | 2a. Rastro por objeto (flag booleana) ✅  | P | NB 09, 10, 13 |
| 2    | 3. Setas / vetores                        | M | NB 04, 08, 09, 11 |
| 3    | 2b. Rastro com janela (`rastro_tempo`)    | M | caso circular na NB 13 |
| 3    | 4. Gráfico sincronizado                   | G | NB 03, 04, 05, 06 |

**Fruta mais baixa:** 2a. Trocar o `deixar_rastro` global por flag no objeto
é um mini-refactor do `desenhar_rastro` — meia tarde de trabalho.

**Mas comece pela 1.** O 2D é pré-requisito dos outros três: rastro em 1D é
só uma linha sobre o eixo (pouco interessante), seta sem 2D só tem um grau
de liberdade, e o gráfico contra posição só faz sentido quando há mais de
uma coordenada. Fazer o 2D primeiro também barateia o 2a: aí o rastro já
nasce útil.

---

### [x] 1. Posição em 2D — NB 08, 09, 10, 11, 13

Alvo: `funcao_movimento(t)` pode devolver escalar (como hoje) ou tupla
`(x, y)`. Se devolver escalar, assume $y = 0$ — retrocompatível com
NB 01–07.

```python
anim.adicionar_objeto("bolinha", 0, lambda t: t, cor="azul")               # 1D
anim.adicionar_objeto("projetil", (0, 0),
                      lambda t: (10*t, 20*t - 0.5*9.8*t**2), cor="azul")   # 2D
```

Passos ([edupils/desafios/cinematica.py](edupils/desafios/cinematica.py)):

- [ ] Em `Objeto`, guardar `posicao` como tupla `(x, y)` internamente;
      no construtor, se vier escalar, armazenar `(posicao, 0)`.
- [ ] Em `Objeto.desenhar`, usar `posicao[0]` e `posicao[1]` em vez de
      `posicao` e `altura`. Manter o parâmetro `altura` só como offset
      extra se fizer falta; idealmente, deletar.
- [ ] Em `Animacao.desenhar_quadro`, aceitar o retorno da
      `funcao_movimento` nas duas formas (escalar ou tupla).
- [ ] Renomear/estender `desenhar_eixo_x` → `desenhar_eixos`, que desenha
      os dois eixos cartesianos. Manter o comportamento antigo quando
      nenhum objeto tem $y \ne 0$ (decisão preguiçosa: sempre desenhar
      os dois — simples e coerente).
- [ ] Em `Animacao.__init__`, adicionar `distancia_em_metros_y`
      (ou renomear para `distancia_em_metros=(dx, dy)`).
- [ ] Sanidade: rodar a NB 07 atual sem mexer no código dela.

### [x] 2a. Rastro por objeto (flag booleana) — NB 09, 10, 13

Mover a flag `deixar_rastro` de `Animacao` para `Objeto`.

```python
anim.adicionar_objeto("projetil", (0, 0), posicao_xy, cor="azul", rastro=True)
```

Passos:

- [ ] Adicionar parâmetro `rastro=False` em `Objeto.__init__` e em
      `Animacao.adicionar_objeto`.
- [ ] Em `Animacao.desenhar_rastro`, iterar só sobre objetos com
      `obj.rastro` (em vez do flag global).
- [ ] Remover `deixar_rastro` de `Animacao.__init__` (quebra de API — a
      NB mais antiga que usa isso precisa de um bump).

### [ ] 3. Setas / vetores — NB 04, 08, 09, 11

Novo tipo de objeto com **origem** e **deslocamento** — ambos funções
de $t$ que devolvem tupla.

```python
anim.adicionar_seta(
    "v_bolinha",
    origem=lambda t: (posicao_x(t), 0),
    deslocamento=lambda t: (velocidade(t), 0),
    cor="vermelho",
)
```

Uma única primitiva cobre:

- vetor velocidade/aceleração sobre um objeto (NB 04, 08, 09);
- decomposição em componentes (duas setas ortogonais — NB 08, 09);
- ponteiro de relógio — origem em $(0,0)$, deslocamento
  $R(\cos\omega t, \sin\omega t)$ (NB 11). *Ponteiro é uma seta girando* —
  não precisa de recurso rotacional separado;
- representação de forças (Módulo 2).

Passos:

- [ ] Adicionar primitiva `desenhar_seta(x0, y0, dx, dy, id_canvas, cor,
      largura)` em [edupils/desenho/desenho.py](edupils/desenho/desenho.py).
      Ponta = triângulo pequeno rotacionado com `rotacionar_ponto` (já
      existe). Corpo = `desenhar_linha`.
- [ ] Criar `class Seta` em `cinematica.py` com `origem(t)`,
      `deslocamento(t)`, `cor`; expor `desenhar(camada)`.
- [ ] `Animacao.adicionar_seta(nome, origem, deslocamento, cor)` e
      guardar em `self.objetos` junto com os outros (polimorfismo
      simples — todos respondem a `desenhar` e têm função de $t$).
- [ ] Tamanho da ponta calibrado em pixels, não em metros (senão some
      quando o deslocamento é pequeno).

### [ ] 2b. Rastro com janela — caso circular (NB 13)

Só necessário quando o rastro se sobrepõe e polui o desenho. Complica
porque precisa guardar histórico.

```python
anim.adicionar_objeto("satelite", (R, 0), orbita,
                      cor="roxo", rastro=True, rastro_tempo=2.0)
```

Passos:

- [ ] Em `Objeto`, manter `historico = deque` de `(t, x, y)`.
- [ ] A cada frame, empilhar a posição; descartar entradas mais antigas
      que `rastro_tempo`.
- [ ] Redesenhar o rastro ligando os pontos do histórico com linhas
      finas (e não mais com snapshot + marca d’água). A marca d’água
      continua disponível para o modo "rastro infinito" do 2a.

### [ ] 4. Gráfico sincronizado — NB 03, 04, 05, 06

Painel novo que compartilha o relógio da animação. Recebe funções de $t$,
desenha as curvas, e um cursor vertical desliza conforme a animação avança.

```python
anim.adicionar_grafico(
    eixo_y="posição [m]",
    curvas={"bolinha": lambda t: posicao(t),
            "carro":   lambda t: 5 + 2*t},
)
```

Passos (mais invasivo — painel separado):

- [ ] Decidir layout: `<canvas>` adicional à direita do atual, ou
      `<div>` irmão. O `criar_painel` já devolve a `<div>` — extender
      para comportar uma segunda área de desenho com três camadas
      próprias (`graficoFundo`, `graficoFrente`).
- [ ] Pré-amostrar as curvas em `adicionar_grafico` para descobrir min/max
      do eixo y (em vez de ficar recalculando no loop).
- [ ] Desenhar eixos + curvas no `graficoFundo` uma única vez.
- [ ] No `desenhar_quadro`, redesenhar só o cursor vertical e os pontos
      `(t, curva(t))` no `graficoFrente`.
- [ ] NB 05 ("soma de pedacinhos"): o aluno constrói as barrinhas com
      as primitivas existentes. Se virar padrão, criar depois um
      `adicionar_barras(t_pontos, alturas, cor)` — **não** priorizar agora.

## Publicação

Ver [HOWTOBUILD.md](HOWTOBUILD.md). Resumindo: basta incrementar a versão em
[setup.py](setup.py) e fazer push para `main`; o workflow
[.github/workflows/workflow.yml](.github/workflows/workflow.yml) constrói a
wheel e publica no PyPI via `twine`.

## Licença

[MIT](LICENSE).
