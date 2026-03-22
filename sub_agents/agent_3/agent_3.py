# sub_agents/agent_3/agent_3.py
# A3 — VTO Architect

from google.adk.agents import LlmAgent
from tools.fashion_tools import generate_virtual_tryon
from tools.callbacks     import ingeniero_inyectar_avatar

agent_3 = LlmAgent(
    name="ecf_vto_architect",
    model="gemini-2.0-flash",

    description=(
        "Especialista en Virtual Try-On y visualización de calce. "
        "Actívame para generar la prueba virtual de una prenda "
        "sobre las medidas reales del usuario."
    ),

    instruction="""
    Eres el VTO Architect de Closet OS.
    Tu ÚNICA responsabilidad: generar el Virtual Try-On.

    PROCESO:
    1. Lee el informe forense del estado (clave: 'forensic_report').
       Si no existe, indica que primero se debe analizar la prenda (A2).
    2. Las medidas del avatar están inyectadas en tu contexto
       (user:avatar_medidas). Úsalas directamente.
       Fallback si no hay medidas: pecho=90, cintura=72, cadera=98.
    3. Llama a generate_virtual_tryon(avatar_data, garment_data).
       - Si status == "error" → informa el problema al usuario.

    OUTPUT KEY: vto_result

    MENSAJES DE TALLA:
    - riesgo_talla == "ok"      → "✅ Ajuste perfecto según tus medidas."
    - riesgo_talla == "pequeño" → "⚠️ Riesgo de ajuste: Pequeño."
    - riesgo_talla == "grande"  → "ℹ️ La prenda puede quedar holgada."
    """,

    tools=[generate_virtual_tryon],

    output_key="vto_result",

    before_model_callback=ingeniero_inyectar_avatar,
)