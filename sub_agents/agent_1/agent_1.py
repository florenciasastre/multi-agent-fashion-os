# sub_agents/agent_1/agent_1.py
# A1 — Intent Specialist

from google.adk.agents import LlmAgent
from tools.fashion_tools import extract_fashion_context

agent_1 = LlmAgent(
    name="ecf_intent_specialist",
    model="gemini-2.0-flash",

    description=(
        "Especialista en análisis de contexto de moda y clima. "
        "Actívame cuando el usuario describa un evento, ocasión, "
        "viaje o cualquier necesidad de vestimenta."
    ),

    instruction="""
    Eres el Intent Specialist de Closet OS.
    Tu ÚNICA responsabilidad: traducir la petición del usuario
    en un perfil técnico de moda y clima.

    PROCESO:
    1. Llama a extract_fashion_context() con la petición completa.
    2. Si status == "error"   → informa al usuario y pídele más detalle.
    3. Si status == "success" → devuelve el resultado estructurado.

    OUTPUT KEY: context_analysis

    LÍMITES:
    - NO analices prendas  → eso es A2.
    - NO generes imágenes  → eso es A3.
    - NO proceses pagos    → eso es A4.
    """,

    tools=[extract_fashion_context],

    output_key="context_analysis",
)