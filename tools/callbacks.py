# tools/callbacks.py
# ─────────────────────────────────────────────────────────────
# Callbacks ECF — TODA la lógica de seguridad centralizada aquí.
#
# 🚪 PORTERO   — before_agent_callback  → valida sesión ECF_
# ⚙️  INGENIERO — before_model_callback  → inyecta user:avatar_medidas
# 🔍 AUDITOR   — before_tool_callback   → bloquea imágenes fraudulentas
#
# MECÁNICA:
#   return None  → 🟢 el flujo continúa normal
#   return valor → 🔴 ejecución detenida
# ─────────────────────────────────────────────────────────────

from typing import Optional

from google.adk.agents.callback_context import CallbackContext
from google.adk.tools import BaseTool, ToolContext
from google.genai import types


# ══════════════════════════════════════════════════════════════
# 🚪 PORTERO — before_agent_callback
# Se asigna al root_agent (ecf_manager).
# Intercepta ANTES de que el LLM consuma un token.
# ══════════════════════════════════════════════════════════════

def portero_validar_sesion(
    callback_context: CallbackContext,
) -> Optional[types.Content]:
    """
    Valida que la sesión sea válida (empieza por ECF_) y bloquea
    intentos de prompt injection antes de invocar cualquier agente.

    Args:
        callback_context (CallbackContext): Contexto con el estado.

    Returns:
        None           → 🟢 sesión válida, el agente continúa.
        types.Content  → 🔴 sesión inválida, el agente se cancela.
    """
    state      = callback_context.state
    session_id = str(state.get("session_id", ""))

    # REGLA: session_id debe empezar por "ECF_"
    if not session_id.startswith("ECF_"):
        print(f"[PORTERO] ⛔ Sesión inválida: '{session_id}'")
        return types.Content(
            role="model",
            parts=[types.Part(text=(
                "⛔ Acceso denegado. Sesión no válida. "
                "Inicia sesión en la plataforma ECF."
            ))]
        )  # 🔴

    # REGLA: bloquear prompt injection
    user_input = str(state.get("user_input", "")).lower()
    forbidden  = [
        "hack", "bypass", "inject", "ignore previous",
        "ignore all", "jailbreak", "forget instructions",
    ]
    if any(t in user_input for t in forbidden):
        print("[PORTERO] ⛔ Prompt injection detectada.")
        return types.Content(
            role="model",
            parts=[types.Part(text=(
                "⛔ Consulta bloqueada por política de seguridad ECF."
            ))]
        )  # 🔴

    print(f"[PORTERO] ✅ Sesión '{session_id}' validada.")
    return None  # 🟢


# ══════════════════════════════════════════════════════════════
# ⚙️  INGENIERO — before_model_callback
# Se asigna al agente A3 (ecf_vto_architect).
# Inyecta user:avatar_medidas en el prompt antes de Gemini.
# ══════════════════════════════════════════════════════════════

def ingeniero_inyectar_avatar(
    callback_context: CallbackContext,
    llm_request,
) -> Optional[object]:
    """
    Inyecta las medidas del avatar en el prompt de A3 antes de que
    Gemini procese el Virtual Try-On. Lee user:avatar_medidas del
    estado persistente (namespace user:).

    Args:
        callback_context (CallbackContext): Contexto con el estado.
        llm_request: Objeto LlmRequest con el prompt actual.

    Returns:
        None siempre. El prompt se modifica in-place (🟢).
    """
    avatar = callback_context.state.get("user:avatar_medidas", {})

    if avatar and isinstance(avatar, dict) and "pecho" in avatar:
        txt = (
            "[SISTEMA — MEDIDAS DEL USUARIO] "
            f"pecho={avatar.get('pecho', '?')}cm, "
            f"cintura={avatar.get('cintura', '?')}cm, "
            f"cadera={avatar.get('cadera', '?')}cm. "
            "Úsalas para calcular riesgo_talla y diferencia_cm."
        )
        if hasattr(llm_request, "contents") and llm_request.contents is not None:
            llm_request.contents.insert(
                0,
                types.Content(role="user", parts=[types.Part(text=txt)])
            )
        print("[INGENIERO] ✅ Medidas del avatar inyectadas.")
    else:
        print("[INGENIERO] ⚠️  Sin avatar. Usando tallas estándar M.")

    return None  # 🟢 siempre


# ══════════════════════════════════════════════════════════════
# 🔍 AUDITOR — before_tool_callback
# Se asigna al agente A2 (ecf_forensic_indexer).
# Bloquea imágenes fraudulentas antes de Computer Vision.
# ══════════════════════════════════════════════════════════════

def auditor_bloquear_fraude(
    tool: BaseTool,
    tool_args: dict,
    tool_context: ToolContext,
) -> Optional[dict]:
    """
    Bloquea imágenes fraudulentas antes de invocar
    forensic_image_analysis(). Detecta bancos de imágenes e IA.
    Si bloquea → Computer Vision nunca se llama → ahorro ~0.15€/intento.

    Args:
        tool (BaseTool): Herramienta que ADK está a punto de ejecutar.
        tool_args (dict): Argumentos que el LLM pasa a la tool.
        tool_context (ToolContext): Contexto de la sesión.

    Returns:
        None  → 🟢 imagen válida, la tool se ejecuta.
        dict  → 🔴 fraude detectado, la tool se CANCELA.
    """
    if tool.name != "forensic_image_analysis":
        return None  # 🟢 no es nuestra herramienta

    url = str(tool_args.get("image_url", "")).lower()

    fraud_signatures = [
        "shutterstock", "gettyimages", "istockphoto", "stock_photo",
        "freepik", "unsplash", "pexels",
        "midjourney", "dall-e", "dalle", "stable_diffusion",
        "ai_generated", "pinterest",
    ]

    if any(sig in url for sig in fraud_signatures):
        print(f"[AUDITOR] 🔴 Imagen fraudulenta bloqueada.")
        return {
            "status":  "error",
            "error":   "FRAUDE_DETECTADO",
            "mensaje": (
                "⚠️ Imagen rechazada: firma de banco de imágenes o IA detectada. "
                "Sube una foto real tomada con tu móvil."
            ),
        }  # 🔴

    print("[AUDITOR] ✅ URL validada. Lanzando análisis forense.")
    return None  # 🟢