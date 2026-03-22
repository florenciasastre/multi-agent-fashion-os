# manager/ecf_manager.py
# ─────────────────────────────────────────────────────────────
# Root Agent — El CEO de Closet OS
#
# tools=[] por diseño absoluto. El Manager NUNCA ejecuta tareas.
# Delega leyendo el campo 'description' de cada sub-agente.
# ─────────────────────────────────────────────────────────────

from google.adk.agents import Agent

# Importación directa — nombres actualizados a la estructura real
from sub_agents.agent_1.agent_1 import agent_1
from sub_agents.agent_2.agent_2 import agent_2
from sub_agents.agent_3.agent_3 import agent_3
from sub_agents.agent_4.agent_4 import agent_4
from tools.callbacks            import portero_validar_sesion

root_agent = Agent(
    name="ecf_manager",
    model="gemini-2.0-flash",

    description=(
        "Gestor central de Closet OS. Coordina el ecosistema de agentes "
        "especializados en moda circular: contexto, peritaje, VTO y pagos."
    ),

    instruction="""
    Eres el Manager de Closet OS — el CEO del sistema.
    Tu rol es EXCLUSIVAMENTE estratégico.

    REGLA DE ORO: No ejecutas tareas. No tienes herramientas.

    DELEGACIÓN — el Manager lee 'description' de cada sub-agente:

    → Usuario describe un evento o necesidad de ropa
      DELEGA a: ecf_intent_specialist

    → Usuario comparte imagen de prenda para analizar
      DELEGA a: ecf_forensic_indexer

    → Usuario quiere ver cómo le queda la prenda
      DELEGA a: ecf_vto_architect

    → Usuario confirma que quiere comprar
      DELEGA a: ecf_logistics_lead

    ESTADO INICIAL REQUERIDO:
    - session_id: debe comenzar por "ECF_"
    - user:avatar_medidas: {"pecho": 90, "cintura": 72, "cadera": 98}
    """,

    tools=[],  # ← VACÍO POR DISEÑO ABSOLUTO

    sub_agents=[agent_1, agent_2, agent_3, agent_4],

    before_agent_callback=portero_validar_sesion,
)