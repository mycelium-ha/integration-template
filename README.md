# My Integration

<!-- Short description of what this Home Assistant integration does. -->

## Installation

### Home Assistant Marketplace (Recommended)

1. Open Home Assistant and go to **Settings > Marketplace**.
2. Click **Add from link** (or search the catalog once published).
3. Enter `https://github.com/mycelium-ha/integration-template` and select **Integration**.
4. Install the integration and complete the setup via **Settings > Devices & Services**.

## Configuration

This integration is configured via the Home Assistant UI (Config Flow). Enter the hostname or IP address of your device.

## Removal

1. Go to **Settings > Devices & Services**, select the integration and delete the entry.
2. Uninstall the integration in **Settings > Marketplace**.

## Development

See [AGENTS.md](AGENTS.md) for conventions and [CONTRIBUTING](https://github.com/mycelium-ha/.github/blob/main/CONTRIBUTING.md) for the workflow.

```bash
python3.14 -m venv .venv && source .venv/bin/activate
pip install -r requirements_test.txt
pip install pre-commit && pre-commit install
pytest --cov
```

## Template checklist (delete after using this template)

- [ ] Run `python3 scripts/rename_integration.py <domain> "<Name>" <repository>`, then delete the script.
- [ ] Replace `api.py` with your device's API (or a PyPI library listed in `manifest.json` `requirements`) and adapt the tests.
- [ ] Check `manifest.json`: `categories` ([list](https://contributors.home-assistant.io/core/integrations/categories/)), `integration_type`, `iot_class`, `codeowners`; set `MANUFACTURER` in `const.py`.
- [ ] Make sure the `@mycelium-ha/maintainers` team exists (or adjust `codeowners` and `.github/CODEOWNERS`).
- [ ] Add brand images (`icon.png`, `icon@2x.png`, `logo.png`, `logo@2x.png`) to `custom_components/<domain>/brand/`, then remove `hacs_ignore: brands` from `.github/workflows/validate.yml`.
- [ ] Update `README.md` with real setup instructions and remove this checklist.
- [ ] Review `quality_scale.yaml`.
- [ ] Bump `version` in `manifest.json` and push a matching `vX.Y.Z` tag for the first release.
