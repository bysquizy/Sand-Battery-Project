"""Source-transparent academic project metadata. Cases are not app calibration data."""
PROJECT={
"title":"Sand Battery Project","product":"Sand Battery Studio",
"institution":"İzmir Institute of Technology (IZTECH)",
"department":"Department of Energy Systems Engineering",
"course":"ESE 101 — Introduction to Energy Systems Engineering",
"academic_year":"Fall 2026/27","group":"Group 8","team_size":3,
"lead_github":"@bysquizy","lead_name":"Yağız Topaç",
"members":("Yağız Topaç", "Semih Cenk", "Fatma Ovacık"),
"repository":"https://github.com/bysquizy/Sand-Battery-Project",
"public_app":"https://sand-battery-project-a5twmepge6cqbndgbz9jmj.streamlit.app/","advisor":"Not specified — confirmation pending",
"affiliation_notice":"Independent student research project for an IZTECH course. Not an official university service or endorsed industrial design.",
}
FIELD_REFERENCES=(
{"site":"Kankaanpää, Finland","year":2022,"thermal_power_mw":0.2,"operator_power_mw":0.1,"thermal_capacity_mwh":8.0,"material":"Sand","evidence":"PNE manufacturer: 200 kW; Vatajankoski operator: 100 kW (unresolved discrepancy)","url":"https://polarnightenergy.com/reference/worlds-first-sand-battery/"},
{"site":"Pornainen, Finland","year":2025,"thermal_power_mw":1.0,"thermal_capacity_mwh":100.0,"material":"Crushed soapstone","evidence":"Manufacturer-stated specification (not model validation)","url":"https://polarnightenergy.com/reference/solution-for-clean-energys-big-problem/"},
)
REFERENCES=(
{"id":"review","group":"Peer-reviewed research","type":"Review article","apa":"Bošnjaković, M., & Santa, R. (2026). Sand batteries for thermal energy storage: A review of operating principles, technologies, challenges and future perspectives. *Clean Technologies, 8*(5), Article 165. https://doi.org/10.3390/cleantechnol8050165","claim":"Technology variants, models, thermophysical properties and research gaps.","url":"https://doi.org/10.3390/cleantechnol8050165"},
{"id":"liu-ltne","group":"Peer-reviewed research","type":"Experimental thermal-model study","apa":"Liu, S., Ahmadi-Senichault, A., Levet, C., & Lachaud, J. (2024). Development and validation of a local thermal non-equilibrium model for high-temperature thermal energy storage in packed beds. *Journal of Energy Storage, 78*, Article 109957. https://doi.org/10.1016/j.est.2023.109957","claim":"Validated methodology in glass-bead packed bed (16 mm); not a calibration for this site's arbitrary material inputs.","url":"https://doi.org/10.1016/j.est.2023.109957"},
{"id":"gifford","group":"Peer-reviewed research","type":"Research article","apa":"Gifford, J., Davenport, P., Wang, X., & Ma, Z. (2024). Fabrication, modeling, and testing of a prototype thermal energy storage containment. *Journal of Solar Energy Engineering, 146*(5), Article 051009. https://doi.org/10.1115/1.4065869","claim":"Validated prototype and model for different high-temperature particle containment.","url":"https://doi.org/10.1115/1.4065869"},
{"id":"kankaanpaa","group":"Manufacturer / field reference","type":"Manufacturer project specification","apa":"Polar Night Energy. (n.d.). *World's first Sand Battery*. https://polarnightenergy.com/reference/worlds-first-sand-battery/","claim":"Kankaanpää (2022): manufacturer currently lists 200 kW and 8 MWh; operator describes 100 kW and 8 MWh.","url":"https://polarnightenergy.com/reference/worlds-first-sand-battery/"},
{"id":"vatajankoski","group":"Operator / field reference","type":"Utility operator description","apa":"Vatajankoski. (n.d.). *Sand Battery*. https://www.vatajankoski.fi/en/projects/sand-battery/","claim":"Operator specification: Kankaanpää 100 kW heat power and 8 MWh storage; differs from Polar Night Energy’s 200 kW statement.","url":"https://www.vatajankoski.fi/en/projects/sand-battery/"},
{"id":"pornainen","group":"Manufacturer / field reference","type":"Manufacturer project specification","apa":"Polar Night Energy. (n.d.). *Solution for clean energy's big problem*. https://polarnightenergy.com/reference/solution-for-clean-energys-big-problem/","claim":"Pornainen (2025): 1 MW thermal, 100 MWh; crushed soapstone.","url":"https://polarnightenergy.com/reference/solution-for-clean-energys-big-problem/"},
{"id":"nrel","group":"National-laboratory research","type":"Lab communication reporting modeled scenario","apa":"National Renewable Energy Laboratory. (2024, March 28). *Solution to energy storage may be beneath your feet*. https://www.nrel.gov/news/features/2024/solution-to-energy-storage-may-be-beneath-your-feet.html","claim":"A distinct particle TES prototype and predicted >95% five-day commercial retention; not this simulator's result.","url":"https://www.nrel.gov/news/features/2024/solution-to-energy-storage-may-be-beneath-your-feet.html"},
{"id":"iztech","group":"Institutional information","type":"Official university website","apa":"İzmir Institute of Technology, Department of Energy Systems Engineering. (n.d.). *Technical and practical information*. https://ese.iyte.edu.tr/en/technical-and-practical-information/","claim":"Official institutional and departmental names.","url":"https://ese.iyte.edu.tr/en/technical-and-practical-information/"},
{"id":"deploy","group":"Software documentation","type":"Official software documentation","apa":"Streamlit. (n.d.). *Deploy your app on Community Cloud*. https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy","claim":"GitHub deployment setup, Python version selection and public URL.","url":"https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy"},
)
COURSE_MILESTONES=(
("2026-11-17","Interim report — tentative course calendar"),
("2027-01-05","Poster presentation — tentative course calendar"),
("2027-01-12","Final report — tentative course calendar"),
)
def bibliography_text():
    return "References (APA-style; review before academic submission)\n\n"+"\n\n".join(ref["apa"].replace("*","") for ref in REFERENCES)+"\n"


# Traceability register: describes the method and the *role* of each reference.
# Linking a source does not calibrate the software to that source.
MODEL_EVIDENCE = (
    {"method":"Sensible heat integral / enthalpy","equation":"Q = m ∫ cp(T) dT",
     "sources":"NREL report 84728; Bošnjaković & Santa (2026) review",
     "evidence":"Thermodynamic method; cp parameters in app are illustrative, not NREL DSC measurements",
     "status":"Analytical method; unvalidated material input"},
    {"method":"0-D thermal storage balance","equation":"m cp(T) dT/dt = P_charge - P_discharge - UA(T − Tamb)",
     "sources":"Energy conservation (first law); simplified cylindrical thermal resistance",
     "evidence":"Numerical energy-closure tests; no field-calibrated heat loss data",
     "status":"Numerically verified, not experimentally validated"},
    {"method":"1-D LTE direct-contact bed","equation":"Transient convection/diffusion with a single local gas/solid temperature",
     "sources":"Bošnjaković & Santa (2026) review",
     "evidence":"General packed-bed research method; not an embedded pipe model",
     "status":"Exploratory numerical model"},
    {"method":"LTNE separate gas–solid 1-D","equation":"Separate gas and solid energy balances; interphase hv(Tgas−Tsolid)",
     "sources":"Liu et al. (2024) DOI:10.1016/j.est.2023.109957",
     "evidence":"Methodological reference from a different glass-bead test apparatus",
     "status":"Numerically exercised, uncalibrated parameters"},
    {"method":"Packed-bed pressure loss","equation":"Ergun viscous + inertial terms",
     "sources":"Ergun packed-bed equation (classical engineering correlation)",
     "evidence":"Direct-contact porous media only; no pipe-geometry hydraulics",
     "status":"Equation-level verification only"},
    {"method":"Heat exchanger","equation":"Q = effectiveness × Cmin × (Th,in − Tc,in)",
     "sources":"Classical effectiveness–NTU method",
     "evidence":"Isolated steady model, not coupled to whole storage plant",
     "status":"Analytical check; no device validation"},
    {"method":"Exergy bound","equation":"X = m ∫ cp(T)(1 − T0/T)dT; Kelvin",
     "sources":"Second-law exergy analysis",
     "evidence":"Upper thermodynamic bound; NOT produced electricity",
     "status":"Analytical method"},
    {"method":"Input uncertainty / LCOH","equation":"Synthetic input perturbations; annualized costs / useful delivered heat",
     "sources":"Transparent scenario assumptions; no vendor quotes",
     "evidence":"Assumed probability distributions and user-set price levels",
     "status":"Illustrative only"},
)
