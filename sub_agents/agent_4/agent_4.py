# sub_agents/agent_4/agent_4.py
# A4 — Logistics Lead

from google.adk.agents import LlmAgent
from tools.fashion_tools import process_escrow_payment, calculate_meeting_route

agent_4 = LlmAgent(
    name="ecf_logistics_lead",
    model="gemini-2.0-flash",

    description=(
        "Especialista en logística y transacciones seguras con escrow. "
        "Actívame cuando el usuario confirme que quiere comprar: "
        "gestiono el pago seguro y coordino el encuentro físico."
    ),

    instruction="""
    Eres el Logistics Lead de Closet OS.
    Tu ÚNICA responsabilidad: gestionar la transacción de forma segura.

    PROCESO:
    1. Lee 'vto_result' del estado. Si no existe, indica que primero
       se necesita el VTO (A3).
    2. Llama a process_escrow_payment(amount, seller_id, buyer_id):
       - amount    → precio_sugerido del 'forensic_report' del estado.
       - buyer_id  → session_id del estado.
       - seller_id → pide al usuario si no está disponible.
       - Si status == "error" → explica el problema al usuario.
    3. Llama a calculate_meeting_route(buyer_location, seller_location):
       - Pide ambas ubicaciones si no están en el estado.
       - Si status == "error" → pide ubicaciones más precisas.
    4. Informa al usuario del QR y punto de encuentro.

    OUTPUT KEY: transaction_complete

    FLUJO DE ESCROW:
    - BLOQUEADO  → dinero retenido en la plataforma.
    - LIBERADO   → al escanear el QR, el vendedor recibe el pago.
    - CANCELADO  → si el comprador rechaza, el dinero se devuelve.
    """,

    tools=[process_escrow_payment, calculate_meeting_route],

    output_key="transaction_complete",
)