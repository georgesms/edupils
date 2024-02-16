import unicodedata

NOME_PAINEL_FUNDO = "painelFundo"
NOME_PAINEL_FRENTE = "painelFrente"
NOME_PAINEL_AUXILIAR = "painelAuxiliar"

COR_PRIMARIA = "#DD00FF"
COR_SECUNDARIA = "#00DDFF"
COR_ESCURA = "#555555"
COR_CLARA = "#F5F5F5"

TRADUCAO_PADRAO_DE_LINHA = {
    "tracejada":"dashed",
    "pontilhada":"dotted",
    "solida":"solid",
    "sólida":"solid",
}

TRADUCAO_CORES = {
    "preto":"black",
    "prata":"silver",
    "cinza":"gray",
    "branco":"white",
    "marrom":"maroon",
    "vermelho":"red",
    "roxo":"purple",
    "fucsia":"fuchsia",
    "verde":"green",
    "lima":"lime",
    "oliva":"olive",
    "amarelo":"yellow",
    "azul-marinho":"navy",
    "azul":"blue",
    "verde-água":"teal",
}


def normalizar_palavra(palavra):
    palavra_normalizada = unicodedata.normalize('NFD', palavra)
    return ''.join(char for char in palavra_normalizada if char.isascii())

def traduzir(palavra, dicionario):
    palavra = normalizar_palavra(palavra)
    palavra = palavra.lower()
    
    if palavra in dicionario:
        return dicionario[palavra]
    return palavra