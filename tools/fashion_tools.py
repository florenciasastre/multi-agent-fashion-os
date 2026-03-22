# tools/fashion_tools.py
# ─────────────────────────────────────────────────────────────
# Custom Tools — Closet OS
#
# REGLA 3 — CONTRATO POR FUNCIÓN:
#   ✓ Docstring semántico: "Usa esta herramienta cuando el usuario..."
#   ✓ Sección Args: con tipo de dato de cada argumento
#   ✓ Sección Returns: con estructura completa del dict
#   ✓ Guard Clauses al inicio: validan cada argumento
#   ✓ return {"status": "error",   "mensaje": str}  → cuando falla
#   ✓ return {"status": "success", ...datos...}     → cuando ok
#
# NOTA: Mocks controlados.
# En producción: reemplaza el cuerpo manteniendo firma y contrato.
# ─────────────────────────────────────────────────────────────

import random
import uuid


# ══════════════════════════════════════════════════════════════
# A1 — Intent Specialist
# ══════════════════════════════════════════════════════════════

def extract_fashion_context(user_query: str) -> dict:
    """
    Usa esta herramienta cuando el usuario describa un evento, ocasión,
    viaje o cualquier necesidad de vestimenta y necesite un perfil técnico
    de moda y clima para orientar su búsqueda de prendas.

    Args:
        user_query (str): Petición cruda del usuario. Mínimo 5 caracteres.
                          Ejemplos:
                            'boda en la playa en Valencia en junio',
                            'look casual para Madrid en invierno',
                            'cena de empresa en Barcelona'.

    Returns:
        dict: Siempre incluye la clave 'status'.
              En éxito:
                {
                  "status":       "success",
                  "temperatura":  str,   # ej: "22C"
                  "estilo":       str,   # ej: "Boho-Chic"
                  "piezas_clave": list,  # ej: ["vestido midi", "sandalias"]
                  "calzado":      str,   # ej: "plano"
                  "evento":       str,   # ej: "boda"
                  "ciudad":       str    # ej: "Valencia"
                }
              En error:
                {"status": "error", "mensaje": str}
    """
    # ── Guard Clauses ─────────────────────────────────────────
    if not user_query or not isinstance(user_query, str):
        return {"status": "error",
                "mensaje": "user_query no puede estar vacío."}
    if len(user_query.strip()) < 5:
        return {"status": "error",
                "mensaje": "Descripción demasiado corta. Añade más detalle sobre el evento."}

    # ── Lógica (Mock — producción: Weather API + análisis semántico) ─
    q = user_query.lower()

    ciudad = "Valencia"
    for c in ["madrid", "barcelona", "sevilla", "bilbao", "málaga", "valencia"]:
        if c in q:
            ciudad = c.capitalize()
            break

    evento = "casual"
    if any(w in q for w in ["boda", "wedding", "casamiento"]):
        evento = "boda"
    elif any(w in q for w in ["trabajo", "oficina", "empresa", "reunión"]):
        evento = "trabajo"
    elif any(w in q for w in ["playa", "beach", "piscina"]):
        evento = "playa"
    elif any(w in q for w in ["fiesta", "noche", "cena", "gala"]):
        evento = "noche"

    catalogo = {
        "boda":    ("Boho-Chic",     ["vestido midi", "sandalias tacón bajo", "bolso de mano"], "tacón bajo"),
        "trabajo": ("Smart Casual",  ["blazer", "pantalón de tela", "camisa"],                  "plano"),
        "playa":   ("Resort Casual", ["vestido ligero", "sandalias planas", "sombrero"],         "plano"),
        "noche":   ("Elegante",      ["vestido de noche", "tacones", "clutch"],                  "tacón"),
        "casual":  ("Casual",        ["jeans", "camiseta básica", "zapatillas"],                 "plano"),
    }
    estilo, piezas, calzado = catalogo[evento]

    return {
        "status":       "success",
        "temperatura":  "22C",
        "estilo":       estilo,
        "piezas_clave": piezas,
        "calzado":      calzado,
        "evento":       evento,
        "ciudad":       ciudad,
    }


# ══════════════════════════════════════════════════════════════
# A2 — Forensic Indexer
# ══════════════════════════════════════════════════════════════

def forensic_image_analysis(image_url: str, required_style: dict) -> dict:
    """
    Usa esta herramienta cuando el usuario comparta la URL de una prenda
    de segunda mano y necesite un análisis pericial: extracción de medidas
    reales de la etiqueta, detección del nivel de desgaste y validación
    de la autenticidad de la marca.

    Args:
        image_url (str): URL HTTPS de la imagen de la prenda.
                         Debe comenzar por 'https://'.
                         Debe ser una foto real, no una imagen de stock.
        required_style (dict): Perfil técnico generado por A1.
                                Clave obligatoria: 'estilo' (str).

    Returns:
        dict: Siempre incluye la clave 'status'.
              En éxito:
                {
                  "status":           "success",
                  "match_porcentaje": float,  # 0.0 – 1.0
                  "wear_level":       str,    # "none" | "light" | "heavy"
                  "cm_pecho":         float,
                  "cm_cintura":       float,
                  "marca_validada":   bool,
                  "precio_sugerido":  float,  # 2 decimales exactos
                  "autenticidad":     str,    # "verificada" | "sospechosa"
                  "descripcion":      str
                }
              En error:
                {"status": "error", "mensaje": str}
    """
    # ── Guard Clauses ─────────────────────────────────────────
    if not image_url or not isinstance(image_url, str):
        return {"status": "error", "mensaje": "image_url no puede estar vacío."}
    if not image_url.startswith("https://"):
        return {"status": "error",
                "mensaje": "La URL debe comenzar por 'https://'. Solo conexiones seguras."}
    if not required_style or not isinstance(required_style, dict):
        return {"status": "error",
                "mensaje": "required_style debe ser un dict. Ejecuta primero A1."}
    if "estilo" not in required_style:
        return {"status": "error",
                "mensaje": "required_style debe tener la clave 'estilo'. Verifica context_analysis."}

    # ── Lógica (Mock — producción: Google Vision API + OCR) ──
    match = round(random.uniform(0.78, 0.98), 2)
    wear  = random.choice(["none", "light"])

    return {
        "status":           "success",
        "match_porcentaje": match,
        "wear_level":       wear,
        "cm_pecho":         88.0,
        "cm_cintura":       72.0,
        "marca_validada":   True,
        "precio_sugerido":  45.00,
        "autenticidad":     "verificada",
        "descripcion":      (
            f"Prenda analizada. Compatibilidad con "
            f"'{required_style['estilo']}': {int(match * 100)}%"
        ),
    }


def check_market_price(brand: str, category: str, wear_level: str) -> dict:
    """
    Usa esta herramienta cuando necesites validar que el precio sugerido
    por el análisis forense es justo comparándolo con el mercado actual
    de segunda mano para esa marca, categoría y estado de uso.

    Args:
        brand (str): Nombre de la marca. No vacío.
                     Ej: "Zara", "Mango", "Massimo Dutti".
        category (str): Tipo de prenda. No vacío.
                        Ej: "vestido", "chaqueta", "pantalón".
        wear_level (str): Estado de uso. Valores válidos:
                          "none"  → como nuevo,
                          "light" → buen estado,
                          "heavy" → muy usado.

    Returns:
        dict: Siempre incluye la clave 'status'.
              En éxito:
                {
                  "status":              "success",
                  "precio_min":          float,
                  "precio_max":          float,
                  "precio_recomendado":  float
                }
              En error:
                {"status": "error", "mensaje": str}
    """
    # ── Guard Clauses ─────────────────────────────────────────
    if not brand or not isinstance(brand, str):
        return {"status": "error", "mensaje": "brand no puede estar vacío."}
    if not category or not isinstance(category, str):
        return {"status": "error", "mensaje": "category no puede estar vacío."}
    allowed = ["none", "light", "heavy"]
    if wear_level not in allowed:
        return {"status": "error",
                "mensaje": f"wear_level inválido: '{wear_level}'. Valores: {allowed}"}

    # ── Lógica (Mock — producción: scraping Vinted/Wallapop) ─
    rangos = {"none": (35, 65), "light": (20, 45), "heavy": (5, 20)}
    mn, mx = rangos[wear_level]

    return {
        "status":             "success",
        "precio_min":         float(mn),
        "precio_max":         float(mx),
        "precio_recomendado": round((mn + mx) / 2, 2),
    }


# ══════════════════════════════════════════════════════════════
# A3 — VTO Architect
# ══════════════════════════════════════════════════════════════

def generate_virtual_tryon(avatar_data: dict, garment_data: dict) -> dict:
    """
    Usa esta herramienta cuando el usuario quiera ver cómo le quedará
    una prenda antes de comprarla, proyectando visualmente la prenda
    sobre las medidas biométricas del avatar del usuario.

    En producción esta función llama a Vertex AI Imagen 3, empaqueta
    los bytes con types.Part.from_bytes(mime_type='image/png') y los
    guarda con client.artifacts.create_artifact(). El agente recibe
    solo el nombre del archivo (puntero ligero, no los bytes).

    Args:
        avatar_data (dict): Medidas biométricas del usuario.
                            Claves requeridas: 'pecho', 'cintura', 'cadera' (float, en cm).
                            Se obtiene del estado 'user:avatar_medidas'.
        garment_data (dict): Informe forense de A2.
                             Clave requerida: 'cm_pecho' (float).

    Returns:
        dict: Siempre incluye la clave 'status'.
              En éxito:
                {
                  "status":        "success",
                  "artifact_name": str,    # ej: "vto_look_v1.png"
                  "riesgo_talla":  str,    # "ok" | "pequeño" | "grande"
                  "diferencia_cm": float,
                  "recomendacion": str
                }
              En error:
                {"status": "error", "mensaje": str}
    """
    # ── Guard Clauses ─────────────────────────────────────────
    if not avatar_data or not isinstance(avatar_data, dict):
        return {"status": "error",
                "mensaje": "avatar_data debe ser un dict con las medidas del usuario."}
    if "pecho" not in avatar_data:
        return {"status": "error",
                "mensaje": "avatar_data debe tener 'pecho'. Verifica 'user:avatar_medidas'."}
    if not garment_data or not isinstance(garment_data, dict):
        return {"status": "error",
                "mensaje": "garment_data debe ser el informe forense de A2."}
    if "cm_pecho" not in garment_data:
        return {"status": "error",
                "mensaje": "garment_data debe tener 'cm_pecho'. Ejecuta primero A2."}
    try:
        avatar_pecho = float(avatar_data["pecho"])
        prenda_pecho = float(garment_data["cm_pecho"])
    except (TypeError, ValueError):
        return {"status": "error", "mensaje": "Las medidas deben ser valores numéricos."}

    # ── Lógica (Mock — producción: Vertex AI + Artifacts API) ─
    diferencia = round(abs(avatar_pecho - prenda_pecho), 1)

    if diferencia <= 2:
        riesgo = "ok"
        rec    = "✅ La prenda debería ajustarse perfectamente a tus medidas."
    elif prenda_pecho < avatar_pecho:
        riesgo = "pequeño"
        rec    = f"⚠️ Riesgo de ajuste: Pequeño. La prenda es {diferencia}cm más estrecha."
    else:
        riesgo = "grande"
        rec    = f"ℹ️ La prenda es {diferencia}cm más amplia. Puede quedar holgada."

    return {
        "status":        "success",
        "artifact_name": f"vto_look_v{random.randint(0, 2)}.png",
        "riesgo_talla":  riesgo,
        "diferencia_cm": diferencia,
        "recomendacion": rec,
    }


# ══════════════════════════════════════════════════════════════
# A4 — Logistics Lead
# ══════════════════════════════════════════════════════════════

def process_escrow_payment(amount: float, seller_id: str, buyer_id: str) -> dict:
    """
    Usa esta herramienta cuando el usuario confirme que quiere comprar
    la prenda y necesites bloquear el pago de forma segura en escrow
    hasta que se produzca la verificación física con QR.

    Args:
        amount (float): Importe en euros. Debe ser > 0 y <= 10000.
        seller_id (str): ID único del vendedor en ECF. No vacío.
        buyer_id (str): ID único del comprador. No vacío.
                        Usa el session_id del estado como buyer_id.
                        No puede coincidir con seller_id.

    Returns:
        dict: Siempre incluye la clave 'status'.
              En éxito:
                {
                  "status":    "success",
                  "escrow_id": str,              # ej: "ESC_A3F2B1C4"
                  "estado":    "bloqueado",
                  "qr_code":   str,              # ej: "QR_9F2A..."
                  "importe":   float,
                  "mensaje":   str
                }
              En error:
                {"status": "error", "mensaje": str}
    """
    # ── Guard Clauses ─────────────────────────────────────────
    if not isinstance(amount, (int, float)):
        return {"status": "error", "mensaje": "amount debe ser un número. Ej: 45.00"}
    if amount <= 0:
        return {"status": "error", "mensaje": f"El importe debe ser > 0. Recibido: {amount}€"}
    if amount > 10000:
        return {"status": "error", "mensaje": f"Importe {amount}€ supera el límite de 10.000€."}
    if not seller_id or not isinstance(seller_id, str):
        return {"status": "error", "mensaje": "seller_id no puede estar vacío."}
    if not buyer_id or not isinstance(buyer_id, str):
        return {"status": "error",
                "mensaje": "buyer_id no puede estar vacío. Usa el session_id del estado."}
    if seller_id == buyer_id:
        return {"status": "error", "mensaje": "seller_id y buyer_id no pueden ser iguales."}

    # ── Lógica (Mock — producción: Mangopay / Stripe Escrow) ─
    escrow_id = f"ESC_{uuid.uuid4().hex[:8].upper()}"
    qr_code   = f"QR_{uuid.uuid4().hex[:12].upper()}"

    return {
        "status":    "success",
        "escrow_id": escrow_id,
        "estado":    "bloqueado",
        "qr_code":   qr_code,
        "importe":   round(amount, 2),
        "mensaje":   (
            f"Pago de {round(amount, 2)}€ bloqueado en escrow. "
            f"QR: {qr_code}. "
            "Muéstraselo al vendedor en el encuentro para liberar el pago."
        ),
    }


def calculate_meeting_route(buyer_location: str, seller_location: str) -> dict:
    """
    Usa esta herramienta cuando necesites calcular el punto de encuentro
    óptimo entre comprador y vendedor después de confirmar el pago en
    escrow, para coordinar la entrega en mano.

    Args:
        buyer_location (str): Barrio o dirección del comprador. Mínimo 3 caracteres.
                              Ej: "Ruzafa, Valencia".
        seller_location (str): Barrio o dirección del vendedor. Mínimo 3 caracteres.
                               Ej: "El Carmen, Valencia".

    Returns:
        dict: Siempre incluye la clave 'status'.
              En éxito:
                {
                  "status":                 "success",
                  "punto_encuentro":        str,
                  "distancia_comprador_km": float,
                  "distancia_vendedor_km":  float,
                  "tiempo_estimado_min":    int
                }
              En error:
                {"status": "error", "mensaje": str}
    """
    # ── Guard Clauses ─────────────────────────────────────────
    if not buyer_location or not isinstance(buyer_location, str):
        return {"status": "error",
                "mensaje": "buyer_location no puede estar vacío. Ej: 'Ruzafa, Valencia'"}
    if len(buyer_location.strip()) < 3:
        return {"status": "error", "mensaje": "buyer_location demasiado corto."}
    if not seller_location or not isinstance(seller_location, str):
        return {"status": "error", "mensaje": "seller_location no puede estar vacío."}
    if len(seller_location.strip()) < 3:
        return {"status": "error", "mensaje": "seller_location demasiado corto."}

    return {
        "status":                 "success",
        "punto_encuentro":        (
            f"Plaza del Ayuntamiento "
            f"(punto medio entre {buyer_location.strip()} y {seller_location.strip()})"
        ),
        "distancia_comprador_km": round(random.uniform(0.5, 3.5), 1),
        "distancia_vendedor_km":  round(random.uniform(0.5, 3.5), 1),
        "tiempo_estimado_min":    random.randint(5, 20),
    }