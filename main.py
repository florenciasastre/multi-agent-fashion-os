# main.py — Motor de Producción Closet OS
import asyncio
from dotenv import load_dotenv

load_dotenv()

from google.adk.runners  import Runner
from google.adk.sessions import InMemorySessionService
from google.genai        import types

from manager.ecf_manager import root_agent

APP_NAME   = "closet_os"
USER_ID    = "usuario_demo_001"
SESSION_ID = "ECF_demo_001"


async def main() -> None:

    # 1. Servicio de sesiones
    session_service = InMemorySessionService()

    # 2. Runner
    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    # 3. Crear sesión con estado inicial
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
        state={
            "session_id": SESSION_ID,
            "user_input": "",
            "user:avatar_medidas": {
                "pecho":   90,
                "cintura": 72,
                "cadera":  98,
            },
        },
    )

    print("\n" + "═" * 50)
    print("  CLOSET OS — Motor de Decisiones de Estilo")
    print("  Google ADK | Multi-Agente | Producción")
    print("═" * 50)
    print(f"  Sesión  : {SESSION_ID}")
    print(f"  Usuario : {USER_ID}")
    print("═" * 50)

    # 4. Consultas de prueba
    consultas = [
        "Busco un look para una boda en la playa en Valencia",
        "Analiza esta prenda: https://mitienda.com/vestido-boho.jpg",
    ]

    for consulta in consultas:
        print(f"\n👤 Usuario: {consulta}")
        print("─" * 50)

        # Formato estricto del mensaje — sin update_session
        mensaje = types.Content(
            role="user",
            parts=[types.Part(text=consulta)],
        )

        # Ejecutar el pipeline
        respuesta_final = None
        async for evento in runner.run_async(
            user_id=USER_ID,
            session_id=SESSION_ID,
            new_message=mensaje,
        ):
            if evento.is_final_response():
                if evento.content and evento.content.parts:
                    respuesta_final = evento.content.parts[0].text

        print(f"🤖 Closet OS: {respuesta_final or '[Sin respuesta]'}")

    # 5. Estado final del pipeline
    print("\n\n📊 Estado del pipeline:")
    print("─" * 50)
    sesion = await session_service.get_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )
    if sesion:
        pipeline_keys = [
            "context_analysis",
            "forensic_report",
            "vto_result",
            "transaction_complete",
        ]
        for clave in pipeline_keys:
            valor = sesion.state.get(clave)
            estado = "✅ escrito" if valor else "⏳ pendiente"
            print(f"   {estado}  →  {clave}")

    print("\n✅ Pipeline completado.\n")


if __name__ == "__main__":
    asyncio.run(main())