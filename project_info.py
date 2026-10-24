"""Source-transparent academic project metadata. Cases are not app calibration data."""
PROJECT={
"title":"Sand Battery Project","product":"Sand Battery Studio",
"institution":"İzmir Institute of Technology (IZTECH)",
"department":"Department of Energy Systems Engineering",
"course":"ESE 101 — Introduction to Energy Systems Engineering",
"academic_year":"Fall 2026/27","group":"Group 8","team_size":3,
"lead_github":"@bysquizy","advisor":"Not specified — confirmation pending",
"affiliation_notice":"Independent student research project for an IZTECH course. Not an official university service or endorsed industrial design.",
}
FIELD_REFERENCES=(
{"site":"Kankaanpää, Finland","year":2022,"thermal_power_mw":0.2,"thermal_capacity_mwh":8.0,"material":"Sand","evidence":"Manufacturer-stated specification (not model validation)","url":"https://polarnightenergy.com/reference/worlds-first-sand-battery/"},
{"site":"Pornainen, Finland","year":2025,"thermal_power_mw":1.0,"thermal_capacity_mwh":100.0,"material":"Crushed soapstone","evidence":"Manufacturer-stated specification (not model validation)","url":"https://polarnightenergy.com/reference/solution-for-clean-energys-big-problem/"},
)
REFERENCES=(
{"id":"review","group":"Peer-reviewed research","type":"Review article","apa":"Bošnjaković, M., & Santa, R. (2026). Sand batteries for thermal energy storage: A review of operating principles, technologies, challenges and future perspectives. *Clean Technologies, 8*(5), Article 165. https://doi.org/10.3390/cleantechnol8050165","claim":"Technology variants, models, thermophysical properties and research gaps.","url":"https://doi.org/10.3390/cleantechnol8050165"},
{"id":"gifford","group":"Peer-reviewed research","type":"Research article","apa":"Gifford, J., Davenport, P., Wang, X., & Ma, Z. (2024). Fabrication, modeling, and testing of a prototype thermal energy storage containment. *Journal of Solar Energy Engineering, 146*(5), Article 051009. https://doi.org/10.1115/1.4065869","claim":"Validated prototype and model for different high-temperature particle containment.","url":"https://doi.org/10.1115/1.4065869"},
{"id":"kankaanpaa","group":"Manufacturer / field reference","type":"Manufacturer project specification","apa":"Polar Night Energy. (n.d.). *World's first Sand Battery*. https://polarnightenergy.com/reference/worlds-first-sand-battery/","claim":"Kankaanpää (2022): 200 kW thermal, 8 MWh.","url":"https://polarnightenergy.com/reference/worlds-first-sand-battery/"},
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
