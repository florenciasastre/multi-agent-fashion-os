from tools.fashion_tools import (
    extract_fashion_context,
    forensic_image_analysis,
    check_market_price,
    generate_virtual_tryon,
    process_escrow_payment,
    calculate_meeting_route,
)


def test_extract_fashion_context_success():
    result = extract_fashion_context("Busco un look para una boda en la playa en Valencia")
    assert result["status"] == "success"
    assert result["evento"] == "boda"
    assert result["ciudad"] == "Valencia"
    assert "estilo" in result


def test_extract_fashion_context_rejects_empty_input():
    result = extract_fashion_context("")
    assert result["status"] == "error"


def test_forensic_image_analysis_requires_https():
    result = forensic_image_analysis("http://example.com/image.jpg", {"estilo": "Boho-Chic"})
    assert result["status"] == "error"


def test_forensic_image_analysis_success_contract():
    result = forensic_image_analysis("https://example.com/image.jpg", {"estilo": "Boho-Chic"})
    assert result["status"] == "success"
    assert result["wear_level"] in ["none", "light", "heavy"]
    assert isinstance(result["precio_sugerido"], float)


def test_check_market_price_validates_wear_level():
    result = check_market_price("Zara", "vestido", "invalid")
    assert result["status"] == "error"


def test_generate_virtual_tryon_fit_risk():
    result = generate_virtual_tryon(
        {"pecho": 90, "cintura": 72, "cadera": 98},
        {"cm_pecho": 88},
    )
    assert result["status"] == "success"
    assert result["riesgo_talla"] in ["ok", "pequeño", "grande"]
    assert "diferencia_cm" in result


def test_process_escrow_payment_rejects_same_buyer_and_seller():
    result = process_escrow_payment(45.0, "user_1", "user_1")
    assert result["status"] == "error"


def test_calculate_meeting_route_success():
    result = calculate_meeting_route("Ruzafa, Valencia", "El Carmen, Valencia")
    assert result["status"] == "success"
    assert "punto_encuentro" in result
