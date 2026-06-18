import anthropic
import logging
import time
from pydantic import BaseModel

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

#molde pydantic para validar la respuesta
class RespuestaAI(BaseModel):
    texto: str
    modelo: str
    tokens_usados: int

class ClienteAI:
    def __init__(self, proveedor="anthropic"):
        self.proveedor = proveedor

        if proveedor == "anthropic":
            self.cliente = anthropic.Anthropic()
            self.modelo = "claude-haiku-4-5"
        else:
            raise ValueError(f"Proveedor no soportado: {proveedor}")
        
        logger.info(f"Cliente iniciado – proveedor: {proveedor}")

    def llamar(self, mensaje, max_tokens=200, reintentos=3):
        logger.info(f"Enviando mensaje: {mensaje[:50]}...")

        for intento in range(reintentos):
            try:
                respuesta = self.cliente.messages.create(
                    model=self.modelo,
                    max_tokens=max_tokens,
                    messages=[{"role": "user", "content": mensaje}]
                    )
                
                #Validar respuesta con pydantic
                resultado = RespuestaAI(
                    texto=respuesta.content[0].text,
                    modelo=respuesta.model,
                    tokens_usados=respuesta.usage.input_tokens + respuesta.usage.output_tokens
                )
                logger.info(f"Respuesta recibida – tokens: {resultado.tokens_usados}")
                return resultado
            
            except anthropic.RateLimitError:
                espera = 2** intento # 1s, 2s, 4s
                logger.warning(f"Rate limit (429) – esperando {espera}s antes de reintentar...")
                time.sleep(espera)

            except anthropic.APIError as e:
                logger.error(f"Error de API {e}")
                raise

        logger.error("Se agotaron los reintentos.")
        raise Exception("No se pudo completar la llamada despues de varios intentos")
    
# Prueba
if __name__ == "__main__":
    cliente = ClienteAI(proveedor="anthropic")
    resultado = cliente.llamar("Di solo el cleinte mejorado funciona")
    print(f"\nTexto: {resultado.texto}")
    print(f"Modelo: {resultado.modelo}")
    print(f"Tokens usados: {resultado.tokens_usados}")