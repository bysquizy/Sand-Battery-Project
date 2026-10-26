"""Reproducible offline engineering report exports without runtime dependencies.

HTML is self-contained with inline vector diagrams and print styles, so the
browser's Print -> Save as PDF gives an accessible visual report. The basic
native PDF is also generated using standard-library PDF 1.4 objects (no
headless browser, TeX, Kaleido or ReportLab service required).
"""
from __future__ import annotations

from dataclasses import asdict
from datetime import date
from html import escape
import io
import math
import textwrap
import unicodedata

import numpy as np

from project_info import PROJECT, REFERENCES
from project_version import APP_VERSION

KEY_RESULTS = (
    ("Theoretical capacity", "capacity_mwh", "MWhth"),
    ("Delivered useful heat", "useful_heat_mwh", "MWhth"),
    ("Modeled source energy", "source_input_mwh", "MWh"),
    ("Charging duration", "charge_hours", "h"),
    ("Standby end temperature", "hold_end_c", "C"),
    ("Discharge duration", "discharge_hours", "h"),
    ("Charging conversion loss", "heater_loss_mwh", "MWh"),
    ("Charging ambient loss", "charge_loss_mwh", "MWh"),
    ("Standby ambient loss", "standby_loss_mwh", "MWh"),
    ("Discharge ambient loss", "discharge_loss_mwh", "MWh"),
    ("Final stored energy vs Tmin", "ending_relative_energy_mwh", "MWh"),
    ("Energy ledger residual", "energy_balance_residual_mwh", "MWh"),
)
DISCLAIMER = (
    "Exploratory, uncalibrated numerical study. NOT experimental validation, "
    "industrial certification, measured efficiency or investment advice."
)


def _validated_payload(scenario, result: dict) -> tuple[list[tuple[str,str]], list[tuple[str,str]]]:
    scenario.validate()
    names = []
    for key, value in asdict(scenario).items():
        if isinstance(value, (int, float)) and not math.isfinite(float(value)):
            raise ValueError("Report scenario contains non-finite values.")
        names.append((key.replace("_", " "), str(value)))
    values = []
    for label, key, unit in KEY_RESULTS:
        number = float(result[key])
        if not math.isfinite(number):
            raise ValueError(f"Report {key} must be finite.")
        values.append((label, f"{number:,.5g} {unit}"))
    return names, values


def _inline_trace_svg(result: dict) -> str:
    sets = []
    for phase, color, xkey, ykey in (
        ("Charge", "#34b9b2", "charge_trace_h", "charge_trace_c"),
        ("Standby", "#5a9ee8", "hold_trace_h", "hold_trace_c"),
        ("Discharge", "#e6a46e", "discharge_trace_h", "discharge_trace_c"),
    ):
        x = np.asarray(result[xkey], dtype=float)
        y = np.asarray(result[ykey], dtype=float)
        if x.size and x.shape == y.shape and np.all(np.isfinite(x)) and np.all(np.isfinite(y)):
            sets.append((phase, color, x, y))
    if not sets:
        return ""
    xmax = max(max(float(x[-1]) for _,_,x,_ in sets), 1)
    ymin = min(float(y.min()) for _,_,_,y in sets) - 20
    ymax = max(float(y.max()) for _,_,_,y in sets) + 20
    h = max(1, ymax-ymin)
    paths = []
    for phase,color,x,y in sets:
        decimate = max(1,math.ceil(len(x)/300))
        indices=list(range(0,len(x),decimate))
        if indices[-1] != len(x)-1:
            indices.append(len(x)-1)
        xy=[f"{54+float(x[i])/xmax*650:.1f},{242-(float(y[i])-ymin)/h*202:.1f}" for i in indices]
        paths.append(f'<polyline class="sb-trace" points="{escape(" ".join(xy))}" fill="none" stroke="{color}" stroke-width="3" />')
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 270" '
            'role="img" aria-label="Computed charging standby and discharging '
            'temperature versus time"><rect width="760" height="270" '
            'rx="14" fill="#0e2435"/>'
            '<path d="M54 24 V242 H712" fill="none" stroke="#8ba3b7" />'
            + ''.join(paths) +
            '<text x="56" y="19" fill="#dcebf5" font-size="13">Computed solid mean temperature vs hours</text>'
            '<text x="655" y="261" fill="#dcebf5" font-size="12">hours</text>'
            '</svg>')


def html_report(scenario, result: dict) -> bytes:
    """One offline-printable UTF-8 HTML file; all source names are escaped."""
    inputs, metrics = _validated_payload(scenario,result)
    inputrows = "".join(f"<tr><th>{escape(k)}</th><td>{escape(v)}</td></tr>"
                        for k,v in inputs)
    metricrows = "".join(f"<tr><th>{escape(k)}</th><td>{escape(v)}</td></tr>"
                         for k,v in metrics)
    citations = "".join(
        f'<li>{escape(ref["apa"].replace("*",""))} '
        f'<a href="{escape(ref["url"],quote=True)}">Source</a></li>'
        for ref in REFERENCES if ref["id"] in ("review","kankaanpaa","pornainen","nrel")
    )
    who=" · ".join(escape(x) for x in PROJECT["members"])
    document = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sand Battery Studio — {escape(scenario.name)}</title>
<style>
:root{{font-family:system-ui,-apple-system,"Segoe UI",Arial,sans-serif;
  color:#e9f4f8;background:#081522;font-size:14px}}
*{{box-sizing:border-box}}
body{{max-width:1080px;margin:36px auto;padding:45px;
  background:radial-gradient(circle at 92% 3%,rgba(68,175,178,.15),transparent 30%),
             linear-gradient(150deg,#10283a,#0c1b2a 65%,#0a1725);
  border:1px solid #355667;border-radius:24px;
  box-shadow:0 35px 85px -50px #000;line-height:1.72}}
h1{{color:white;margin:8px 0 10px;letter-spacing:-.045em;
  font-size:clamp(29px,4.2vw,47px);line-height:1.13}}
h2{{font-size:19px;margin:27px 0 12px;letter-spacing:-.025em;
  color:#d6f7f1;break-after:avoid}}
p{{color:#d1e2eb;margin:10px 0 15px}}
.eyebrow{{letter-spacing:.17em;color:#75ebd5;font-weight:800;font-size:11px}}
.grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:22px}}
section{{background:rgba(17,39,55,.86);border:1px solid #3b5b6d;
  border-radius:16px;padding:19px 22px;min-width:0}}
section h2{{margin-top:0}}
table{{width:100%;border-collapse:collapse;font-size:12.5px}}
td,th{{padding:10px 7px;text-align:left;border-bottom:1px solid #294758;vertical-align:top}}
th{{width:59%;font-weight:680;color:#cfe0e8}}
td{{color:#f5f8fb;font-variant-numeric:tabular-nums;overflow-wrap:anywhere}}
tr:last-child td,tr:last-child th{{border-bottom:0}}
.warn{{padding:15px 20px;background:rgba(126,90,44,.19);
  border-left:4px solid #efc18f;border-radius:0 11px 11px 0;
  color:#f6e1c6;font-weight:660}}
a{{color:#84e4d2;text-decoration-color:#528f8a;overflow-wrap:anywhere}}
a:hover{{color:#fff}}
svg{{display:block;width:100%;max-width:100%;height:auto;
  border:1px solid #3a5869;border-radius:15px;margin:25px auto}}
ol{{padding-left:22px}}li{{color:#c9dce6;margin:0 0 12px}}
strong{{color:#f0f9fc}}
small,.muted{{color:#bacfdc}}
.sb-trace{{stroke-dasharray:1400;stroke-dashoffset:1400;
  animation:sb-chart-reveal 1.7s ease-out both}}
@keyframes sb-chart-reveal{{to{{stroke-dashoffset:0}}}}
@media(max-width:690px){{
  body{{margin:0;border-radius:0;padding:19px}}
  .grid{{grid-template-columns:1fr;gap:14px}}
  section{{padding:15px}}
  h1{{font-size:30px}}
}}
@media(prefers-reduced-motion:reduce){{
  .sb-trace{{animation:none;stroke-dashoffset:0}}
}}
@media print{{
  :root{{color:#142d3a;background:white;font-size:11px}}
  body{{max-width:none;margin:0;padding:6mm;background:white;
    color:#142d3a;border:0;border-radius:0;box-shadow:none}}
  h1,h2,strong{{color:#173f4b}}
  h1{{font-size:26px}}
  p,li,td,th,small,.muted{{color:#1d3c4c}}
  .eyebrow{{color:#186c69}}
  .grid{{gap:11px}}
  section{{background:white;border:1px solid #ccdce2;padding:13px;break-inside:avoid}}
  section h2{{color:#195d64}}
  td,th{{border-color:#d3dfe5;padding:6px}}
  .warn{{background:#fff7ec;color:#6b471c;border-color:#ba7830}}
  .sb-trace{{animation:none;stroke-dashoffset:0}}
  a{{color:#126070}}
  svg{{break-inside:avoid}}
  @page{{size:A4;margin:12mm}}
}}
</style></head><body>
<div class="eyebrow">GROUP 8 · ENGINEERING SCENARIO · SOFTWARE v{APP_VERSION}</div>
<h1>Sand Battery Studio — Scenario Report</h1>
<p><strong>{escape(scenario.name)}</strong> · {date.today().isoformat()}</p>
<p class="warn">{escape(DISCLAIMER)}</p>
{_inline_trace_svg(result)}
<div class="grid"><section><h2>Input design</h2><table>{inputrows}</table></section>
<section><h2>Calculated results</h2><table>{metricrows}</table></section></div>
<h2>Model and interpretive limits</h2>
<p>0-D uniform storage temperature; approximate cylindrical envelope UA; illustrative
bulk density and cp(T); charging source represented by the selected input assumption;
constant useful thermal discharge rating until Tmin. No experimental calibration,
radial temperature field, pump work or guaranteed outlet temperature.</p>
<p><strong>Conservation:</strong> source energy = conversion losses + ambient losses +
useful heat + final relative stored energy (numerical residual listed above).
A small ledger residual is not measured device efficiency.</p>
<h2>Selected underlying evidence</h2><ol>{citations}</ol>
<h2>Provenance & credits</h2>
<p>Sand Battery Studio · {who}. Academic simulation by Group 8.
<a href="{escape(PROJECT["repository"],quote=True)}">Project repository</a>.
Materials and parameters are inputs, not measurements. Verify literature at source.</p>
<p class="muted"><small>HTML contains inline SVG; it does not load external scripts or fonts.
Use the browser's Print / Save as PDF for the richly styled printable edition.</small></p>
</body></html>"""
    return document.encode("utf-8")


def _pdf_safe(value: str) -> str:
    # Base PDF Helvetica cannot encode Turkish dotless-i etc. The HTML edition
    # retains complete Unicode names. Transliteration avoids corrupt PDF bytes.
    replacements = {"ı":"i","İ":"I","ğ":"g","Ğ":"G","ş":"s","Ş":"S","ç":"c","Ç":"C"}
    normalized="".join(replacements.get(ch,ch) for ch in value)
    return unicodedata.normalize("NFKD",normalized).encode("ascii","replace").decode("ascii")


def _pdf_escaped(value: str) -> str:
    return _pdf_safe(value).replace("\\","\\\\").replace("(","\\(").replace(")","\\)")


def pdf_report(scenario, result: dict) -> bytes:
    """Basic multi-page offline PDF 1.4 report; pure stdlib and no extra fonts.

    Printable HTML preserves full UTF-8 and has an SVG graphic; this PDF is a
    compact, text-first snapshot with a vector KPI visual.
    """
    inputs, metrics = _validated_payload(scenario,result)
    data = [
        ("Sand Battery Studio | v"+APP_VERSION, True),
        ("Group 8 -- modeled engineering scenario",False),
        ("Scenario: "+scenario.name,False), (" ",False),
        (DISCLAIMER,False), (" ",False),
        ("NUMERICAL RESULTS",True),
    ] + [(f"{k}: {v}",False) for k,v in metrics] + [
        (" ",False),("SCENARIO PARAMETERS",True)
    ] + [(f"{k}: {v}",False) for k,v in inputs] + [
        (" ",False),("PHYSICAL ASSUMPTIONS AND LIMITS",True),
        ("0-D uniform solid temperature, assumed material cp(T) and bulk density.",False),
        ("Simplified cylindrical thermal loss; no measured calibration.",False),
        ("Constant source and useful delivery powers. No pump/fan work.",False),
        ("Energy residual checks arithmetic, not field validation.",False),
        (" ",False),("EVIDENCE AND TEAM",True),
        ("Bošnjakovic and Santa (2026), Clean Technologies 8(5), 165.",False),
        ("https://doi.org/10.3390/cleantechnol8050165",False),
        ("Polar Night Energy: world-first sand battery (200 kW / 8 MWh).",False),
        ("https://polarnightenergy.com/reference/worlds-first-sand-battery/",False),
        ("Manufacturer ratings are NOT simulator calibration data.",False),
        ("Group 8: "+", ".join(PROJECT["members"]),False),
        (PROJECT["repository"],False),
    ]
    # 53 wrapped lines per A4 page at 12pt leading; keeps pages predictable.
    wrapped=[]
    for txt,heading in data:
        lines=textwrap.wrap(_pdf_safe(txt),width=92,break_long_words=False,
                            break_on_hyphens=False) or [""]
        for k,line in enumerate(lines):
            wrapped.append((line,heading and k==0))
    pages=[wrapped[i:i+48] for i in range(0,len(wrapped),48)]
    n=len(pages)
    objects = [b""] # object 0 unused; indices start at 1
    def add(payload: bytes) -> int:
        objects.append(payload);return len(objects)-1
    font=add(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    contents=[]
    for i,rows in enumerate(pages):
        commands=["0.10 0.19 0.27 rg",
                  "0.28 0.70 0.68 RG", "0.8 w",
                  "44 785 m 551 785 l S"]
        for j,(line,heading) in enumerate(rows):
            y=763-j*14.5
            commands += [
                ("0.13 0.40 0.44 rg" if heading else "0.12 0.18 0.23 rg"),
                f"BT /F1 {11 if heading else 9.6} Tf 1 0 0 1 46 {y:.2f} Tm ({_pdf_escaped(line)}) Tj ET",
            ]
        commands += [f"0.5 0.58 0.62 rg BT /F1 9 Tf 1 0 0 1 46 25 Tm (Group 8  |  {i+1}/{n}  |  Numerical research only) Tj ET"]
        body="\n".join(commands).encode("ascii")
        contents.append(add(b"<< /Length "+str(len(body)).encode()+b" >>\nstream\n"+body+b"\nendstream"))
    pages_index=add(b"")
    page_objects=[]
    for content in contents:
        page_objects.append(add(
            f"<< /Type /Page /Parent {pages_index} 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 {font} 0 R >> >> /Contents {content} 0 R >>".encode()
        ))
    objects[pages_index]=(f"<< /Type /Pages /Count {n} /Kids ["
                          + " ".join(f"{p} 0 R" for p in page_objects)
                          + "] >>").encode()
    catalog=add(f"<< /Type /Catalog /Pages {pages_index} 0 R >>".encode())
    buf=io.BytesIO()
    buf.write(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets=[0]
    for index,payload in enumerate(objects[1:],1):
        offsets.append(buf.tell())
        buf.write(f"{index} 0 obj\n".encode())
        buf.write(payload)
        buf.write(b"\nendobj\n")
    start=buf.tell()
    buf.write(f"xref\n0 {len(objects)}\n0000000000 65535 f \n".encode())
    for offset in offsets[1:]:
        buf.write(f"{offset:010d} 00000 n \n".encode())
    buf.write(f"trailer\n<< /Size {len(objects)} /Root {catalog} 0 R >>\nstartxref\n{start}\n%%EOF\n".encode())
    return buf.getvalue()
