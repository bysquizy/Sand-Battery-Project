# Security Policy

## Project status

Sand Battery Studio is an academic research preview, **not** a production service or a safety-certified engineering tool. Simulations are not sufficient for construction, investment or plant operations.

## Supported versions

| Version | Security support |
| --- | --- |
| 1.0 alpha (`main`) | Best-effort review by student maintainers; no response-time guarantee |
| Older releases | Not supported |

## Report a vulnerability

**Do not publish secrets, exploit instructions or sensitive information in public issues.**

If private vulnerability reporting has been enabled by the repository owner, select **Security → Advisories → Report a vulnerability**. Otherwise contact the owner privately using a contact method that they have chosen to publish on their GitHub profile. If no private channel exists, open a *non-sensitive* issue requesting a private contact path—without exploit details.

Provide the affected version, expected/actual behavior and safe reproduction steps. The maintainers will review reports on a best-effort basis. Adding this policy does not automatically enable GitHub's private vulnerability reporting.

## Safe research and software use

- Never commit credentials, personal information, `.env` files or `.streamlit/secrets.toml`.
- Review and update third-party Python dependencies.
- Treat material data and simulated thermal performance as unvalidated research estimates.
