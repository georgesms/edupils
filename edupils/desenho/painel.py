from js import document

# Function to create a canvas with specific attributes
def criar_painel(id, width, height):
    painel = document.createElement("canvas")
    painel.setAttribute("id", id)
    painel.width = width
    painel.height = height
    painel.style.position = "absolute"
    painel.style.left = 0
    painel.style.top = 0
    return painel

def apagar_painel(id_painel):
    painel = document.getElementById(id_painel)
    contexto = painel.getContext('2d')
    contexto.clearRect(0, 0, painel.width, painel.height)


def criar_painel(camadas_auxiliares=1, largura=500, altura=300):
    
    div = document.createElement("div")
    div.setAttribute("id", "gameCanvas")
    div.style.setProperty("position", "relative")
    div.style.setProperty("width", f"{largura}px")
    div.style.setProperty("height", f"{altura}px")

    for nome_painel in ["painelFundo", "painelAuxiliar", "painelFrente"]:
        painel = criar_painel(nome_painel, largura, altura)
        div.appendChild(painel)

    return div
    