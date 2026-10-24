"""Source-transparent, *hypothetical* granular medium comparisons.

Packed densities, cp coefficients and blend results below are SCENARIO VALUES
and not lab certifications; suitability near 573 C or with residues is unknown.
"""
from .materials import Material

SCENARIOS={
"Quartz sand (NREL bulk-density scenario)": Material("Quartz sand (NREL bulk-density scenario)",1543,740,.90,"1543 kg/m3 from NREL report 84728; cp curve is NOT their measured DSC data"),
"Foundry sand (illustrative)": Material("Foundry sand (illustrative)",1550,790,.55,"Assumption; possible trace-metal/organic contamination"),
"Granite aggregate (illustrative)": Material("Granite aggregate (illustrative)",1650,790,.45,"Assumption; mineralogy and packing untested"),
"River gravel (illustrative)": Material("River gravel (illustrative)",1720,840,.30,"Assumption; density and cp untested"),
"Quartzite (illustrative)": Material("Quartzite (illustrative)",1710,770,.60,"Assumption; possible quartz inversion at 573 C"),
"Olivine (illustrative)": Material("Olivine (illustrative)",1860,900,.30,"Assumption; no specimen measured"),
"Alumina beads (illustrative)": Material("Alumina beads (illustrative)",2000,810,.35,"Assumption: packed granules, not solid density"),
"Cordierite pellets (illustrative)": Material("Cordierite pellets (illustrative)",1600,850,.20,"Assumption; untested material grade"),
"Recycled concrete (illustrative)": Material("Recycled concrete (illustrative)",1550,850,.25,"Potential water and chemical stability limitations"),
"Steel slag (illustrative)": Material("Steel slag (illustrative)",1900,820,.30,"Composition-dependent; expansion and contamination risks"),
"Blast-furnace slag (illustrative)": Material("Blast-furnace slag (illustrative)",1660,840,.30,"Environmental compliance and thermal behavior untested"),
"Reclaimed fireclay (illustrative)": Material("Reclaimed fireclay (illustrative)",1700,790,.45,"Assumption; test refractory grade and thermal cycling"),
"Fly-ash aggregate (illustrative)": Material("Fly-ash aggregate (illustrative)",1200,850,.25,"Hypothetical; leaching and air-quality testing required"),
}
