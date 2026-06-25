# Architecture Notes

## Core Principle

Closet OS separates four responsibilities:

1. Agent orchestration.
2. Tool execution.
3. Session state.
4. Safety callbacks.

The manager agent only routes. It does not execute business logic.

## Agent Flow

1. User describes a fashion need.
2. The manager delegates to the intent specialist.
3. If a garment image is provided, the forensic indexer analyzes it.
4. The VTO architect evaluates fit against avatar measurements.
5. The logistics lead simulates escrow and meeting-point coordination.

## Production Upgrade Path

The current tool bodies are controlled mocks. The function signatures and return contracts should remain stable while replacing the internal logic with real integrations.

Recommended next upgrades:

- Replace `extract_fashion_context` with weather API + semantic extraction.
- Replace `forensic_image_analysis` with multimodal image analysis and OCR.
- Replace `check_market_price` with marketplace pricing data.
- Replace `generate_virtual_tryon` with a VTO model.
- Replace `process_escrow_payment` with a real payment provider.
- Replace `calculate_meeting_route` with a Maps API.
