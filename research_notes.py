"""Research reading notes distilled from the user-supplied documents.

These are editorial summaries for educational use, not copied excerpts.
Article sections are cited explicitly; uncertainty and source class are retained.
"""
REVIEW = {
    "title": "Sand Batteries for Thermal Energy Storage: A Review of Operating Principles, Technologies, Challenges and Future Perspectives",
    "authors": "Mladen Bošnjaković and Robert Santa",
    "publication": "Clean Technologies 8(5), 165 (2026)",
    "doi": "https://doi.org/10.3390/cleantechnol8050165",
}
TOPICS = (
    {
        "id":"basics","label":"How sand thermal storage works","section":"§3.1, Charging / Storage / Discharging",
        "summary":"A sand battery is sensible thermal energy storage: heat is placed in a granular solid, kept for a period, and recovered for a heat load. Charging, standby losses and heat extraction must be considered as separate operating phases.",
        "key_points":(
            "Charging may use surplus renewable electricity and an electric heater or another specified thermal source.",
            "Insulation and the actual heat-transfer path govern standby losses.",
            "Heat at a useful delivery temperature is a stricter metric than ideal theoretical stored heat.",
        ),
        "model":"Dashboard 0-D charging, standby and thermal-output simulation",
        "limitation":"The application's mean-temperature 0-D model does not reproduce the outlet-temperature limits of a real exchanger.",
        "equation":"Q = m × ∫ cp(T) dT",
    },
    {
        "id":"technology","label":"Storage architecture families","section":"§3.2, Types of Technologies",
        "summary":"The review distinguishes fixed packed beds, thermocline beds, fluidized beds, moving beds, hybrid sand–PCM arrangements and enhanced-conductivity concepts. These configurations have different flow, mixing and heat-transfer behaviors.",
        "key_points":(
            "A thermocline is a spatial hot–cold transition, not a label for every sand container.",
            "Moving and fluidized particles change the contact and transport mechanisms.",
            "The closed-loop embedded-pipe commercial architecture must not be treated as the same geometry as a direct-contact 1-D bed.",
        ),
        "model":"The direct-contact LTE/LTNE research model is provided as a separate exploratory scenario.",
        "limitation":"No fluidized-bed, moving-bed or sand–PCM latent-heat model has been calibrated in this app.",
        "equation":"Architecture-specific gas and solid energy balances",
    },
    {
        "id":"material","label":"Storage media and high temperatures","section":"§3.1–3.2 and §6.2–6.3",
        "summary":"Bulk packing density, temperature-dependent heat capacity, conductivity, durability and cycling conditions jointly affect stored energy and accessible heating power. Cheap aggregate is not automatically suitable at all temperatures.",
        "key_points":(
            "Distinguish bulk density, solid density and the void fraction of a packed medium.",
            "Low effective conductivity can limit power even when theoretical thermal capacity is large.",
            "Quartz-rich materials have an α–β transition near 573 °C; a smooth linear cp(T) demonstration cannot capture its enthalpy signature.",
        ),
        "model":"Material Atlas compares illustrative media and cp(T) slopes.",
        "limitation":"Most medium parameters are scenario assumptions, not sample-specific calorimetry or durability results.",
        "equation":"E_th = ρ_bulk V ∫[Tmin,Tmax] cp(T) dT",
    },
    {
        "id":"thermal","label":"Heat transfer, losses and thermocline","section":"§3.2.2, §4.1, §6.3–6.4",
        "summary":"Heat travels through particles, exchanger surfaces and insulation; the useful temperature field is non-uniform in real storage systems. Thermocline spreading and losses may reduce useful recoverable heat.",
        "key_points":(
            "0-D mean-temperature simulations trade geometric detail for speed and traceability.",
            "1-D studies resolve one spatial dimension and require boundary conditions and mesh tests.",
            "A visual 3D silo animation is not CFD and does not prove a measured radial/axial field.",
        ),
        "model":"Dashboard 0-D, design cooling/insulation, and the direct-contact LTE/LTNE pages.",
        "limitation":"No 3-D CFD, calibrated wall bridging or actual embedded-pipe geometry is solved.",
        "equation":"m cp(T) dT/dt = P_in − P_out − UA(T−Tamb)",
    },
    {
        "id":"renewables","label":"Renewable input and heat delivery","section":"§1, §3.1 and §6.6",
        "summary":"Solar and wind supply vary over time, while thermal demand can be continuous. Scheduling charging around cheap or surplus electricity is a system-level question, distinct from the thermal storage material itself.",
        "key_points":(
            "Installed PV/wind capacity is not the same as dispatchable, hourly available power.",
            "Commercial sand thermal storage primarily supplies heat; reconverting it into electricity adds conversion losses.",
            "The useful heat output must respect a defined end-use temperature and exchanger capacity.",
        ),
        "model":"Electric/CSP/PV-wind scenarios and the hypothetical hourly renewable-dispatch research tab.",
        "limitation":"Built-in renewable traces are synthetic scenarios, not a verified site forecast or operator schedule.",
        "equation":"E_input = ∫ P_available(t) dt;  E_delivered ≤ E_useful",
    },
    {
        "id":"simulation","label":"Numerical modelling and AI","section":"§4, Modelling and Optimisation",
        "summary":"The review discusses CFD, machine learning, physics-informed models and possible digital twins. Their suitability depends on the amount and relevance of validation data—not on whether a plot appears smooth.",
        "key_points":(
            "Numerical convergence and energy conservation are necessary tests but do not demonstrate agreement with measurements.",
            "A physics-informed model for one packed-bed apparatus does not validate a different closed-loop silo.",
            "A digital twin requires ongoing operational measurements and an updated physical model, neither of which this project has.",
        ),
        "model":"Deterministic numerical solvers, sensitivity cases and regression tests; no external AI inference is needed.",
        "limitation":"The website is an educational simulator, not a real-time IoT digital twin.",
        "equation":"Residual = E_in − E_losses − E_delivered − ΔE",
    },
    {
        "id":"economics","label":"Economics and sustainability","section":"§5.1–5.2 and §6.5–6.6",
        "summary":"Lifecycle analysis must consider materials, charging-energy cost, exchanger and insulation equipment, installation, maintenance and end-of-life impacts. Low-cost sand alone does not imply low delivered-heat cost.",
        "key_points":(
            "Clearly separate CAPEX, OPEX, annual delivered thermal energy and electricity purchase assumptions.",
            "Thermal LCOH is not comparable to electricity LCOE or electrical round-trip efficiency without aligning system boundaries.",
            "Environmental claims require lifecycle data and consistent functional units.",
        ),
        "model":"Research Lab's assumption-driven levelized cost of heat and parametric studies.",
        "limitation":"No sourced vendor quote or lifecycle inventory is loaded; values are hypothetical.",
        "equation":"LCOH ≈ (annualized CAPEX + O&M + annual input cost) / annual delivered MWhth",
    },
    {
        "id":"safety","label":"Safety, reliability and adoption barriers","section":"§5.3–5.4 and §6",
        "summary":"A noncombustible storage medium does not remove risks from hot surfaces, heaters, electrical systems, pressure boundaries, particulate contamination or thermal stress. Design maturity and regulatory requirements differ across sites.",
        "key_points":(
            "Thermal cycling and heterogeneous waste materials need specimen-specific stability testing.",
            "Mechanical integrity, fire/electrical safety and operations procedures are not assessed by heat-capacity equations.",
            "Long-term reliability and reference-plant reporting should not be inferred from a student numerical model.",
        ),
        "model":"Explicit out-of-scope warnings and conservative input bounds in the software.",
        "limitation":"No equipment certification, pressure-vessel calculations, fail-safe controls or physical sensors are included.",
        "equation":"Technical risk ≠ a single efficiency number",
    },
)
AUDIT = {
    "title":"Sand Battery Source Check — Enhanced Research Audit",
    "meaning":"P1/P2 identify provenance (original source/operator vs manufacturer-reported information), not whether a simulator result is measured or certified.",
    "tiers":{
        "P1":"Original institutional, laboratory, project-operator or original-publisher record.",
        "P2":"Named manufacturer statement or company-provided operational statistic.",
        "S1":"Specialist journalism accurately citing identifiable sources.",
        "S2":"Secondary syndication, snippets, mirrors or indirectly available text.",
        "U":"Underlying original source not opened or unavailable.",
    },
    "verdicts":{
        "MATCH":"Specific wording supported by the cited source.",
        "QUALIFY":"Requires time, scope, conditionality or status clarification.",
        "MISATTRIBUTED":"Possibly correct in substance, but the named reference does not support it.",
        "CONTRADICTED":"Direct conflict with a checked source.",
        "NOT LOCATED":"Claim not found in the inspected material.",
        "UNRESOLVED":"Conflicting original sources or insufficient access.",
    },
}
SOURCE_NOTES=(
    {"title":"2026 research review","class":"Peer-reviewed review","supports":"Technology families, sensible heat, modelling, energy economics, risks and knowledge gaps.","not_valid":"Not a calibration dataset for this software.","url":REVIEW["doi"]},
    {"title":"Polar Night Energy technical summary","class":"Manufacturer-provided material (team upload)","supports":"Closed-loop heat-transfer description, heat services and selected commercial-project context.","not_valid":"Company projections and marketing claims are not independent performance tests.","url":"https://polarnightenergy.com/"},
    {"title":"Enhanced Source Check audit","class":"Team source-quality document","supports":"Provenance grades, corrected attribution and unresolved claims.","not_valid":"It is not a full independent experimental certification.","url":""},
    {"title":"NREL particle TES material example","class":"National laboratory","supports":"Sample-specific high-purity silica bulk-density / cp evidence and quartz-transition concern.","not_valid":"Do not substitute into this project's illustrative material curves without complete measured dataset and domain check.","url":"https://www.nrel.gov/docs/fy23osti/84728.pdf"},
)
