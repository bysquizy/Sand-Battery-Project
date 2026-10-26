# Security Policy

## Scope and status

Sand Battery Studio is a public, simulation-only academic web application. Its numerical results do **not** certify equipment, industrial performance, safety or investment suitability.

## Supported versions

| Version | Security support |
| --- | --- |
| 1.4.x (`main` after release) | Best-effort fixes by the Group 8 maintainers |
| Earlier releases and historical beta branches | Not actively supported |

The GitHub repository and the [live website](https://sand-battery-project-a5twmepge6cqbndgbz9jmj.streamlit.app/) are publicly readable. There is no promised response SLA.

## Private security reports

**Do not submit credentials, unpublished personal information or actionable exploit details to public GitHub issues.**

If GitHub's private vulnerability reporting is available, use **Security → Advisories → Report a vulnerability**. Otherwise reach a maintainer using a private contact method published on their GitHub profile. If no private route is available, open only a non-sensitive issue requesting a private contact channel; do not include exploit details.

Include the affected version/commit, the impacted page or upload path and safe reproduction steps.

## Safeguards

- Keep `.streamlit/secrets.toml`, `.env` and API credentials out of the repository.
- Uploaded CSV content is bounded by size, row count, finite numeric values and allowed power ranges before simulation.
- Treat rate/CPU and memory protection as resource limits, not a security guarantee.
- Update dependencies only after tests pass; investigate Dependabot alerts.
- Do not disable Streamlit's default XSRF/CORS defenses in a shared development container.

This security policy does not assert an independent penetration test or a certified security audit.
