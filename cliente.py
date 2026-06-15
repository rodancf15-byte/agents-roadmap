import anthropic
import logging

# Configuracion basica de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ClienteAI:
    def __init__(self, proveedor="anthropic"):
        self.proveedor = proveedor

        if proveedor == "anthropic":
            self.cliente = anthropic.Anthropic()
            self.modelo = "claude-haiku-4-5"
        else:
            raise ValueError(f"Proveedor no soportado: {proveedor}")
        
        logger.info(f"Cliente iniciado – proveedor: {proveedor}")
    
    def llamar(self, mensaje, max_tokens=200):
        logger.info(f"Enviando mensaje: {mensaje[:50]}...")

        respuesta = self.cliente.messages.create(
            model=self.modelo,
            max_tokens=max_tokens,
            messages=[
                {"role": "user", "content": mensaje}
            ]
        )

        texto =  respuesta.content[0].text
        logger.info(f"Respuesta recibida: {texto[:50]}...")
        return texto
    


# Prueba basica
if __name__ == "__main__":
    cliente = ClienteAI(proveedor="anthropic")
    respuesta = cliente.llamar("Di solo: el cliente funciona.")
    print(f"\nRespuesta: {respuesta}")