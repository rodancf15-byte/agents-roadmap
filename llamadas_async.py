import asyncio
import anthropic

cliente = anthropic.Anthropic()

async def llamar_claude(numero):
    try:
        respuesta = cliente.messages.create(
            model="claude-haiku-4-5",
            max_tokens=100,
            messages=[
                {"role": "user", "content": f"Di solo: soy la llamada número {numero}"}
            ]
        )
        texto = respuesta.content[0].text
        print(f"Llamada {numero}: OK")
        return texto
    except Exception as error:
        print(f"Llamada {numero}: ERROR — {error}")
        return None

async def main():
    tareas = [llamar_claude(i) for i in range(1, 11)]
    resultados = await asyncio.gather(*tareas)
    exitosas = [r for r in resultados if r is not None]
    print(f"\n{len(exitosas)} de 10 llamadas completadas exitosamente.")

asyncio.run(main())
