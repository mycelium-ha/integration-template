# Agent and contributor guide

Conventions for this Home Assistant custom integration. Humans and coding agents follow the same rules.

## Layout

- `custom_components/my_integration/`: the integration
  - `api.py`: device/service client (no Home Assistant imports)
  - `coordinator.py`: `DataUpdateCoordinator` and the typed `MyIntegrationConfigEntry`
  - `entity.py`: base entity (device info, `has_entity_name`)
  - platform modules (`sensor.py`, ...) use entity descriptions
  - `quality_scale.yaml`: Integration Quality Scale status, kept current
- `tests/`: pytest against real Home Assistant (`pytest-homeassistant-custom-component`)
- `scripts/check_translations.py`: `strings.json` and `translations/*.json` must stay in sync

## Rules

- Async only; never block the event loop. Use the shared aiohttp session (`async_get_clientsession`).
- Per-entry objects live in `entry.runtime_data`, never in `hass.data`.
- Flow schemas use `probatio` (Home Assistant's successor of voluptuous).
- Every user-facing string goes through `strings.json` and every file in `translations/` (entity names, errors, exceptions).
- Raise translated exceptions (`translation_domain`/`translation_key`).
- Entities get a stable `unique_id`; config entries get a `unique_id` from the device, not the host.
- Diagnostics redact everything that identifies the user, their devices or their network.
- Typed Python; `mypy --strict` must pass.
- Update `quality_scale.yaml` when a rule changes status.

## Checks (all must pass before a PR)

```bash
ruff check . && ruff format --check .
mypy
python scripts/check_translations.py
pytest --cov
```

CI runs the same checks plus `hassfest` and the Marketplace/HACS validation through the shared workflows of [mycelium-ha/.github](https://github.com/mycelium-ha/.github).

## Releases

Bump `version` in `manifest.json`, merge, push a matching `vX.Y.Z` tag. `release.yml` verifies the version and publishes the GitHub release.
