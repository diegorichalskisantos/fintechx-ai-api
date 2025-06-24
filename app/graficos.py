import matplotlib.pyplot as plt
import io
import base64

def gerar_grafico_barra_base64(labels, valores, titulo=""):
    plt.figure(figsize=(10, 6))
    plt.barh(labels, valores, color='skyblue')
    plt.xlabel("Quantidade")
    plt.title(titulo)
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)

    imagem_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    return f"data:image/png;base64,{imagem_base64}"
