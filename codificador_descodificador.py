import base64

def codificar_base64(texto):
    # Convertir el string a bytes
    bytes_texto = texto.encode('utf-8')
    
    # Codificar los bytes en base64
    base64_bytes = base64.b64encode(bytes_texto)
    
    # Convertir los bytes base64 a un string
    base64_texto = base64_bytes.decode('utf-8')
    
    return base64_texto


def decodificar_base64(texto_codificado):
    # Convertir el string base64 a bytes usando utf-8
    base64_bytes = texto_codificado.encode('utf-8')
    
    # Decodificar los bytes base64
    bytes_decodificados = base64.b64decode(base64_bytes)
    
    # Convertir los bytes decodificados a un string usando utf-8
    texto_original = bytes_decodificados.decode('utf-8')
    
    return texto_original

