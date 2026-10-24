# Source Register and Claim Boundaries

## Materials provided by Group 8 (non-redistributed)

1. **`kum-bataryasi-proje-main.zip`** — original single-file Python/Streamlit model: volume and cylinder geometry, sensible enthalpy, equivalent thermal resistance, 0-D charging and discharge, 1-D thermocline and source scenarios. Used as a *reference for reimplementation*; the original script is deliberately not copied into this public code package.
2. **`Sand Battery Reasearch Polar Night Energy.docx`** — manufacturer-sourced account of high-temperature solid TES using an air loop and embedded heat-transfer pipes; water, air and steam outputs. Manufacturer claims are not independent measurements.
3. **`Sand_Battery_Source_Check_Enhanced_Research_Audit.docx`**, second edition 24 October 2026 — internal source-verification matrix; highlights thermal/electrical energy distinctions, attribution corrections, 85%/95% efficiency boundary conditions and projected versus observed emissions.
4. **`Sand battery report for thermal energy.docx`** — copy of Bošnjaković & Santa (2026) journal review. Technical classification, materials and modeling techniques.
5. **`ESE101_Fall 2026-27_Information Sheet 1.pdf`**, **`ESE101_Fall 2026-27_tentative course calendar.docx`** — course reporting obligations and deadlines. Not stored in this public repository to avoid sharing non-project personal information.

## Public primary and review references

Bošnjaković, M., & Santa, R. (2026). Sand batteries for thermal energy storage: A review of operating principles, technologies, challenges and future perspectives. *Clean Technologies, 8*(5), 165. https://doi.org/10.3390/cleantechnol8050165

Polar Night Energy. (n.d.). *Sand battery*. https://polarnightenergy.com/sand-battery/

National Renewable Energy Laboratory. (2024, March 28). *Solution to energy storage may be beneath your feet*. https://www.nrel.gov/news/features/2024/solution-to-energy-storage-may-be-beneath-your-feet.html

Vatajankoski. (n.d.). *Sand battery*. https://www.vatajankoski.fi/en/projects/sand-battery/

Streamlit. (n.d.). *Install Streamlit using command line*. https://docs.streamlit.io/get-started/installation/command-line

Streamlit. (n.d.). *Deploy your app on Community Cloud*. https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy

## Engineering epistemology

- **Engineering identity and mass balance:** geometry and heat-capacity equations are physically general, subject to model boundary definitions.
- **Parameter examples:** density, cp25, cp slope and insulation conductivity are inherited simplified assumptions, not certificates. Each medium needs temperature-dependent measurements and a proper uncertainty range.
- **Energy efficiencies:** electricity-to-useful-heat over the simulated full cycle is not electricity-to-electricity round-trip efficiency.
- **1-D visualization:** LTE through-bed conceptual finite-volume model; cannot directly validate the pipe-in-sand architecture of a commercial silo.
- **Seasonal storage:** stand-by heat retention alone does not prove heat can be delivered continuously at the required outlet temperature.
- **NREL retention/cost values:** refer to a distinct moving-particle system and modeled cases; do not transfer to this geometry.
- **No project outputs are experimentally calibrated** without an appropriate source measurement dataset.


## Public web-release verification — 24 October 2026

- University name: **İzmir Institute of Technology (IZTECH)**; department: **Department of Energy Systems Engineering**, based on https://ese.iyte.edu.tr/en/technical-and-practical-information/.
- Kankaanpää (2022), **unresolved rating discrepancy**: Polar Night Energy's manufacturer page lists **200 kW thermal / 8 MWh** (https://polarnightenergy.com/reference/worlds-first-sand-battery/); owner/operator Vatajankoski lists **100 kW thermal / 8 MWh** (https://www.vatajankoski.fi/en/projects/sand-battery/). Both are directly attributable sources. Preserve the difference, rather than calling either output rating independently verified for this project's simulation. The uploaded Enhanced Source Verification & Research Audit correctly treats it as unresolved.
- Pornainen: **1 MW thermal / 100 MWh**, 2025, crushed soapstone, from https://polarnightenergy.com/reference/solution-for-clean-energys-big-problem/.
- NREL's **>95% thermal retention over five days** is a **modeled commercial-scale outcome for a distinct particle TES architecture** supported by prototype work, NOT a measurement of this project or of Polar Night Energy's plant: https://www.nrel.gov/news/features/2024/solution-to-energy-storage-may-be-beneath-your-feet.html.
- The bibliography displayed in the website is maintained in `project_info.py`, with APA-style entries and a claim-evidence mapping. None of these public references certifies the app's uncalibrated material inputs or heat delivery figures.
