# My Integration

[![Release](https://img.shields.io/github/v/release/mycelium-ha/integration-template?style=for-the-badge)](https://github.com/mycelium-ha/integration-template/releases)
[![Home Assistant](https://img.shields.io/badge/dynamic/json?url=https://raw.githubusercontent.com/mycelium-ha/integration-template/main/hacs.json&query=%24.homeassistant&prefix=%E2%89%A5%20&label=Home%20Assistant&color=41BDF5&style=for-the-badge)](https://www.home-assistant.io/)
[![Validate](https://img.shields.io/github/actions/workflow/status/mycelium-ha/integration-template/validate.yml?branch=main&label=checks&style=for-the-badge)](https://github.com/mycelium-ha/integration-template/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

<!-- One sentence for users: what does this bring into Home Assistant? Lead with the benefit, not the technology. -->
**Bring your My Manufacturer devices into Home Assistant**: live values, set up entirely in the UI.

My Integration (`my_integration`) talks to your device over the local network. It is part of [Mycelium HA](https://github.com/mycelium-ha).

## Features

<!-- What users get (Quality Scale: docs-supported-functions). Keep it to what works today. -->
- A sensor for the device's current value
- Setup and address changes entirely in the UI
- Diagnostics that are safe to share (addresses and serial numbers removed)

## Supported devices

<!-- Exact models that are known to work (docs-supported-devices). Mark untested models as such. -->
| Device | Status |
| --- | --- |
| My Manufacturer Example Device | Tested |

Missing your device? [Request it](https://github.com/mycelium-ha/integration-template/issues/new?template=device_request.yml).

## Requirements

- Home Assistant (minimum version as shown in the badge above)
- The device on the same network as Home Assistant

## Installation

1. In Home Assistant, open **Settings → Marketplace**.
2. Search for **My Integration**, or choose **Add from link** and enter `https://github.com/mycelium-ha/integration-template`.
3. Install it and restart Home Assistant.

## Configuration

[![Open your Home Assistant instance and start setting up My Integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=my_integration)

Or go to **Settings → Devices & services → Add integration** and search for **My Integration**.

<!-- Every field of the setup dialog (docs-installation-parameters). -->
| Field | Description |
| --- | --- |
| Host | The hostname or IP address of your device |

If the device gets a new address, set it up again with the new address; Home Assistant recognizes the device and updates the existing entry.

## How data is updated

<!-- Polling interval or push, and what happens when the device is offline (docs-data-update). -->
The integration asks the device for new values every minute. If the device can't be reached, its entities become unavailable until it answers again.

## Examples

<!-- One or two automations that show a real use case (docs-examples, docs-use-cases). -->
```yaml
automation:
  - alias: "Notify when the value is high"
    triggers:
      - trigger: numeric_state
        entity_id: sensor.my_device_value
        above: 30
    actions:
      - action: notify.notify
        data:
          message: "My Device reports {{ states('sensor.my_device_value') }}"
```

## Known limitations

<!-- What doesn't work or isn't supported, and why (docs-known-limitations). -->
- None known yet.

## Troubleshooting

<!-- Common problems and their fix (docs-troubleshooting). -->
- **"Failed to connect" during setup:** check that the address is correct and that Home Assistant can reach the device on your network.
- **Entities are unavailable:** the device didn't answer the last update; check its power and network connection.

When you report a problem, attach the diagnostics (**Settings → Devices & services → My Integration → ⋮ → Download diagnostics**) and debug logs (**⋮ → Enable debug logging**, reproduce the problem, then disable it to download the log).

## Removal

1. Go to **Settings → Devices & services**, select **My Integration** and delete the entry.
2. Uninstall it in **Settings → Marketplace** and restart Home Assistant.

## Contributing

Bug reports, device tests, translations and code are welcome; see [contributing](https://github.com/mycelium-ha/.github/blob/main/CONTRIBUTING.md). Developers start with [AGENTS.md](AGENTS.md):

```bash
python3.14 -m venv .venv && source .venv/bin/activate
pip install -r requirements_test.txt
pip install pre-commit && pre-commit install
pytest --cov
```

---

<sub>My Integration is an independent community project of [Mycelium HA](https://github.com/mycelium-ha). It is not affiliated with My Manufacturer, Home Assistant, the Open Home Foundation or Nabu Casa.</sub>

<!--
## Template checklist (delete this block after using the template)

- [ ] Run `python3 scripts/rename_integration.py <domain> "<Name>" <repository>`, then delete the script.
- [ ] Replace `api.py` with your device's API (or a PyPI library listed in `manifest.json` `requirements`) and adapt the tests.
- [ ] Check `manifest.json`: `categories` (https://contributors.home-assistant.io/core/integrations/categories/), `integration_type`, `iot_class`, `codeowners`; set `MANUFACTURER` in `const.py` and replace "My Manufacturer" in this README.
- [ ] Add brand images (`icon.png`, `icon@2x.png`, `logo.png`, `logo@2x.png`) to `custom_components/<domain>/brand/`, then remove `hacs_ignore: brands` from `.github/workflows/validate.yml`.
- [ ] Fill in every README section above (each comment names the Quality Scale rule) and delete the comments.
- [ ] Run `scripts/apply-repo-standards.sh <repository>` from mycelium-ha/.github.
- [ ] Create a social preview with `branding/generate_social_preview.py` in mycelium-ha/.github and upload it in the repository settings.
- [ ] Add the integration to the catalog table in mycelium-ha/.github `profile/README.md`.
- [ ] Review `quality_scale.yaml`.
- [ ] Bump `version` in `manifest.json` and push a matching `vX.Y.Z` tag for the first release.
-->
