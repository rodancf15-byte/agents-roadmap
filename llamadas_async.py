import asyncio
import anthropic

cliente = anthropic.Anthropic()

async def llamar_claude(numero):
    respuesta = cliente.messages.create(
        model="claude-haiku-4-5",
        max_tokens=100,
        messages=[
            {"role": "user", "content": f"Di solo: soy la llamada número {numero}"}
        ]
    )
    texto = respuesta.content[0].text
    print(f"Llamada {numero}: {texto}")
    return texto

async def main():
    tareas = [llamar_claude(i) for i in range(1, 4)]
    resultados = await asyncio.gather(*tareas)
    print("\nTodas las llamadas completadas.")

asyncio.run(main())