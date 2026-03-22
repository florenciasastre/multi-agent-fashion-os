# sub_agents/agent_2/agent_2.py
# A2 — Forensic Indexer

from google.adk.agents import LlmAgent
from tools.fashion_tools import forensic_image_analysis, check_market_price
from tools.callbacks     import auditor_bloquear_fraude

agent_2 = LlmAgent(
    name="ecf_forensic_indexer",
    model="gemini-2.0-flash",

    description=(
        "Especialista en análisis pericial de prendas de segunda mano. "
        "Actívame cuando haya una imagen de prenda que analizar: "
        "detecto desgaste, extraigo medidas reales y valido autenticidad."
    ),

    instruction="""
    Eres el Forensic Indexer de Closet OS.
    Tu ÚNICA responsabilidad: analizar prendas con precisión forense.

    PROCESO:
    1. Lee el perfil del estado compartido (clave: 'context_analysis').
       Si no existe, pide al usuario que describa primero el evento.
    2. Llama a forensic_image_analysis(image_url, required_style).
       - Si status == "error" → informa el motivo al usuario.
    3. Opcionalmente llama a check_market_price() para validar el precio.

    OUTPUT KEY: forensic_report

    REGLAS:
    - precio_sugerido: exactamente 2 decimales.
    - wear_level: solo "none", "light" o "heavy".
    """,

    tools=[forensic_image_analysis, check_market_price],

    output_key="forensic_report",

    before_tool_callback=auditor_bloquear_fraude,
)