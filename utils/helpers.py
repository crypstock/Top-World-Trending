import datetime

def formatear_fecha():
    """Devuelve la fecha actual en formato YYYY-MM-DD."""
    return datetime.datetime.now().strftime("%Y-%m-%d")

def limpiar_texto(texto):
    """Elimina caracteres innecesarios de un texto."""
    return texto.strip().replace("\n", "").replace("\r", "")

def dividir_lista(lista, tamanio):
    """Divide una lista en sublistas más pequeñas."""
    return [lista[i:i + tamanio] for i in range(0, len(lista), tamanio)]
