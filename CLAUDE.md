# CLAUDE.md

Orientações para trabalhar neste repositório.

## Para quem é este código

O público-leitor **não é um desenvolvedor profissional** — é um aluno avançado
de ensino médio que está aprendendo a programar e, ao mesmo tempo, estudando
o conteúdo que o código ilustra (física, geometria, algoritmos). O código é
lido em aula, em notebooks Starboard rodando Pyodide.

Isso significa que **as decisões de design priorizam legibilidade para
iniciantes**, não robustez de engenharia.

## Princípios

### 1. Tudo em português

Nomes de classes, funções, parâmetros, variáveis e mensagens: **sempre em
português**. Inclusive palavras como `largura`, `altura`, `cor`, `raio`,
`posicao`, `velocidade` — e não `width`, `height`, `color` etc.

As cores e padrões de linha aceitos pelas funções devem passar por
[constantes.traduzir](edupils/constantes.py) para que o aluno possa escrever
`"vermelho"` ou `"tracejada"` naturalmente.

### 2. Rústico > sofisticado

Prefira **soluções simples e diretas** mesmo que um pouco repetitivas.
Evite:

- Metaclasses, decoradores elaborados, descriptors.
- Hierarquias profundas de classes quando uma função já resolve.
- Padrões de projeto (Factory, Strategy, Observer…) quando um `if` resolve.
- Compreensões aninhadas quando dois `for` explícitos são mais claros.
- Generalizações para casos que ainda não apareceram.

A pergunta-guia é: *“um aluno consegue ler isto de cima a baixo e entender
o que acontece?”*. Se a resposta é não, simplifique.

### 3. Pouco defensivo

Não adicione validação de tipos, checagem de entrada, try/except, nem
fallbacks para situações que não vão ocorrer no uso didático. Erros
informativos em português (como os de [fisica/grandezas.py](edupils/fisica/grandezas.py))
são bem-vindos **quando fazem parte do conteúdo que está sendo ensinado**
(ex: somar metros com segundos). Fora disso, confie na entrada.

### 4. Sem docstrings longos nem comentários redundantes

Não descreva o que o código já diz. Comente só quando há um *porquê*
não-óbvio (uma sutileza matemática, um detalhe do canvas, um contorno de
bug do Pyodide). Docstrings extensos no estilo Google/NumPy não combinam
com o tom do projeto.

### 5. Nada de tipagem estática

Não introduzir `typing`, `@dataclass`, `Protocol`, anotações `-> None`,
etc. Os módulos existentes são deliberadamente sem tipos.

### 6. Dependências enxutas

O [requirements.txt](requirements.txt) está vazio de propósito —
preferimos usar apenas a stdlib e o que já vem no Pyodide (`numpy` quando
necessário). Antes de adicionar uma dependência, pergunte ao usuário.

## Ambiente de execução

A maior parte do código roda **dentro do navegador** via Pyodide e
desenha sobre `<canvas>` usando `from js import document`. Consequências:

- `import edupils.desenho` quebra fora do Pyodide — isso é esperado.
- Animações usam `async`/`await` com `asyncio.sleep` porque o loop de
  eventos é o do browser.
- Testes unitários em [tests/](tests/) estão praticamente vazios; não
  invista tempo em cobertura a menos que o usuário peça.

### Arquitetura do canvas

Três camadas empilhadas, criadas por [desenho/painel.py](edupils/desenho/painel.py):

| Camada             | Uso típico                                           |
|--------------------|------------------------------------------------------|
| `painelFundo`      | cenário estático (labirinto, eixos), rastros         |
| `painelAuxiliar`   | elementos persistentes desenhados pelo aluno (tartaruga traça linhas aqui) |
| `painelFrente`     | atores que são redesenhados a cada frame             |

O padrão de animação é: `apagar_painel(painelFrente)` →  redesenhar os
atores → `await asyncio.sleep(dt)`.

## Fluxo de publicação

1. Incrementar a versão em [setup.py](setup.py).
2. `git push` para `main`.
3. O workflow [.github/workflows/workflow.yml](.github/workflows/workflow.yml)
   faz o build da wheel e publica no PyPI com `twine`.

Não crie tags nem releases manualmente — o workflow dispara em todo push
para `main`.

## Estrutura

```
edupils/
├── constantes.py    # cores, dimensões, traduções PT→EN
├── desenho/         # primitivas de canvas (depende de js.document)
├── desafios/        # atividades prontas: tartaruga, labirinto, cinemática
├── fisica/          # vetor, grandezas com unidade, forças, motor de simulação
├── imagem/          # placeholder
└── sons/            # placeholder
```

Ao adicionar um novo desafio, coloque-o em `desafios/` e siga o padrão
dos existentes: uma classe principal que já se desenha no construtor e
expõe métodos no vocabulário do aluno (`mover`, `virar`, `andar`…).