"""Sand Battery Studio design system.

CSS and HTML are trusted source literals only. No external fonts, JS, CDNs,
cookies, client-side scripts or untrusted HTML injection.
Streamlit's native controls remain accessible and functional.
"""
from __future__ import annotations

from html import escape
import streamlit as st

CSS = """
<style>
:root {
  --sb-bg:#07121d;
  --sb-surface:#101f2d;
  --sb-glass:#132637;
  --sb-line:#2e495a;
  --sb-ink:#eff7fb;
  --sb-muted:#bed0db;
  --sb-teal:#68e5cf;
  --sb-gold:#f2c18c;
  --sb-blue:#7bb8ed;
}
html,body,[data-testid="stApp"] {
  font-family:system-ui,-apple-system,"Segoe UI",Arial,sans-serif;
}
[data-testid="stApp"] {
  background:radial-gradient(ellipse 60% 410px at 74% -80px,rgba(64,176,177,.18),transparent 80%),
             radial-gradient(ellipse 43% 430px at 0% 19%,rgba(239,176,112,.085),transparent 85%),
             linear-gradient(160deg,#081522 0%,#081421 65%,#07111b 100%);
  color:var(--sb-ink);
}
[data-testid="stMainBlockContainer"],.block-container {
  max-width:1360px;
  padding-top:1.2rem;
  padding-bottom:4rem;
}
[data-testid="stSidebar"] {
  background:linear-gradient(170deg,#0c1d2a 0%,#071420 100%);
  border-right:1px solid var(--sb-line);
}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
  color:#cbdce5;
}
[data-testid="stSidebarNav"] a {
  border-radius:10px;
  transition:background-color .18s ease,color .18s ease;
}
[data-testid="stSidebarNav"] a:hover{background:#1c3b47}
[data-testid="stSidebarNav"] a[aria-current="page"] {
  background:#1e444b;
  color:#e7fff8;
}
h1,h2,h3 {letter-spacing:-.034em;color:#f4f9fc;text-wrap:balance}
h1 {font-size:clamp(1.9rem,3.1vw,2.65rem);font-weight:790;line-height:1.18}
h2 {font-size:clamp(1.32rem,2vw,1.78rem);font-weight:750}
h3 {font-size:1.18rem;font-weight:730}
[data-testid="stCaptionContainer"],.stCaption {
  color:var(--sb-muted);
  line-height:1.6;
}
[data-testid="stMetric"] {
  position:relative;
  padding:18px 19px 17px;
  min-height:126px;
  background:linear-gradient(145deg,rgba(31,57,70,.87),rgba(14,29,45,.97));
  border:1px solid #3b5869;
  border-radius:17px;
  box-shadow:inset 0 1px rgba(255,255,255,.055),0 12px 28px -25px #000;
}
[data-testid="stMetric"]:before {
  content:"";
  position:absolute;
  top:0;left:20px;right:20px;height:2px;
  background:linear-gradient(90deg,var(--sb-teal),rgba(104,229,207,0));
  opacity:.8;
}
[data-testid="stMetricLabel"] p {
  color:#d0dfe7;
  font-weight:700;
  font-size:.78rem;
  letter-spacing:.075em;
  text-transform:uppercase;
}
[data-testid="stMetricValue"] {
  color:#fff;
  font-size:clamp(1.32rem,2.2vw,1.85rem);
  font-weight:790;
  letter-spacing:-.03em;
  overflow-wrap:anywhere;
}
[data-testid="stMetricDelta"]{color:var(--sb-teal)}
[data-testid="stPlotlyChart"] {
  background:linear-gradient(145deg,#112638,#0d1c2b);
  border:1px solid #355366;
  border-radius:17px;
  padding:7px 4px;
  overflow:hidden;
  box-shadow:0 10px 35px -31px #000;
}
[data-testid="stDataFrame"] {
  border:1px solid #355467;
  border-radius:12px;
  overflow:hidden;
}
[data-testid="stExpander"],[data-testid="stForm"],
[data-testid="stVerticalBlockBorderWrapper"] > div[data-testid="stVerticalBlock"] {
  border-color:#355264;
}
[data-testid="stAlert"]{border-radius:13px;line-height:1.5}
[data-testid="stDownloadButton"] button,
[data-testid="stButton"] button,
[data-testid="stLinkButton"] a {
  border-radius:11px;
  font-weight:730;
  min-height:2.55rem;
  transition:background-color .18s ease,border-color .18s ease,box-shadow .18s ease;
}
[data-testid="stButton"] button[kind="primary"],
[data-testid="stLinkButton"] a[kind="primary"] {
  background:linear-gradient(115deg,#173b46,#225a62);
  border:1px solid #367986;
  color:#effffc;
  box-shadow:0 8px 23px -19px #f2c18c;
}
[data-testid="stButton"] button:hover,
[data-testid="stLinkButton"] a:hover {
  border-color:#80d9ce;
  box-shadow:0 8px 23px -21px #80d9ce;
}
[data-testid="stRadio"] label,[data-testid="stToggle"] label {
  line-height:1.48;
}
[data-testid="stTabs"] button[role="tab"] {
  color:#c9d8e2;
  font-weight:720;
}
[data-testid="stTabs"] button[aria-selected="true"] {color:var(--sb-teal)}
[data-testid="stTabs"] [data-baseweb="tab-highlight"] {background:var(--sb-teal)}
.sb-eyebrow {
  font-size:.80rem;
  color:var(--sb-teal);
  text-transform:uppercase;
  letter-spacing:.19em;
  font-weight:790;
}
.sb-hero {
  position:relative;
  overflow:hidden;
  isolation:isolate;
  border:1px solid #49737f;
  border-radius:25px;
  padding:clamp(24px,4vw,48px);
  margin:10px 0 23px;
  background:radial-gradient(circle at 88% 16%,rgba(109,225,209,.18),transparent 35%),
             linear-gradient(117deg,#193b46 0%,#102838 56%,#122032 100%);
  box-shadow:0 25px 50px -41px rgba(0,0,0,.85),inset 0 1px rgba(255,255,255,.065);
}
.sb-hero:after{
  content:"";position:absolute;z-index:-1;
  width:min(37vw,380px);aspect-ratio:1;right:-85px;top:-135px;
  border-radius:50%;border:30px solid rgba(242,193,140,.11);
  box-shadow:0 0 0 33px rgba(104,229,207,.05),0 0 0 70px rgba(242,193,140,.035);
  animation:sb-intro 1.25s ease-out both;
}
.sb-hero h1{
  max-width:790px;
  font-size:clamp(2.05rem,4.5vw,3.55rem);
  font-weight:820;
  letter-spacing:-.05em;
  line-height:1.1;
  margin:15px 0 18px;
  color:#fff;
}
.sb-hero p{max-width:750px;color:#d1e4eb;font-size:1rem;line-height:1.75;margin:0}
.sb-hero .sb-kicker{
  display:inline-block;
  margin-right:9px;
  padding:5px 11px;
  border-radius:999px;
  border:1px solid #40847e;
  background:#153d3f;
  font-size:.76rem;font-weight:790;
  letter-spacing:.08em;
  color:#a5f6df;
}
.sb-section-intro{
  display:flex;align-items:center;flex-wrap:wrap;gap:9px;
  color:#a8c5d3;font-size:.86rem;font-weight:660;
  margin:5px 0 13px;
  letter-spacing:.065em;
  text-transform:uppercase;
}
.sb-section-intro:before{
  content:"";display:inline-block;width:17px;height:4px;
  border-radius:9px;background:var(--sb-teal);
}
.sb-context{
  display:flex;gap:9px;align-items:center;flex-wrap:wrap;
  border:1px solid #345466;
  border-radius:12px;
  padding:11px 14px;
  margin:5px 0 15px;
  background:linear-gradient(100deg,rgba(25,57,70,.9),rgba(12,30,43,.68));
}
.sb-context-label {
  font-size:.72rem;
  font-weight:800;
  text-transform:uppercase;
  letter-spacing:.14em;
  color:var(--sb-teal);
  margin-right:4px;
}
.sb-chip{
  font-size:.79rem;
  border:1px solid #3c6370;
  background:#162f3d;
  color:#e0edf3;
  border-radius:999px;
  padding:4px 9px;
  max-width:100%;
  overflow-wrap:anywhere;
}
.sb-note {
  padding:14px 17px;
  border-left:3px solid var(--sb-gold);
  border-radius:0 11px 11px 0;
  background:rgba(28,49,65,.84);
  color:#d1e1e9;
  font-size:.88rem;
  line-height:1.66;
}
.sb-footer{
  margin-top:34px;
  border-top:1px solid #355365;
  padding-top:17px;
  color:#bbceda;
  font-size:.81rem;
  line-height:1.7;
}
.sb-footer a{color:#9feadb}
.hero,.info-line,.sect,.label-block,.foot{ /* legacy compatibility */
  color:inherit;
}
.hero{
  border-radius:23px;
  padding:31px 35px;
  margin:7px 0 24px;
  border:1px solid #49717d;
  background:linear-gradient(115deg,#193c46,#112736 62%,#142636);
}
.hero h1{font-size:clamp(2rem,3.7vw,3rem);color:#fff;letter-spacing:-.045em}
.hero p{font-size:.97rem;color:#d0e1e9;line-height:1.7}
.eyebrow{font-size:.81rem;font-weight:790;letter-spacing:.13em;color:var(--sb-teal)}
.pill{display:inline-block;padding:5px 10px;border-radius:20px;
  border:1px solid #427d77;color:#a4f6e0;background:#163d3f}
.info-line{border-left:3px solid var(--sb-gold);padding:13px 17px;
  border-radius:0 11px 11px 0;background:#152e3d;color:#d1e1e9;
  font-size:.9rem;margin:14px 0}
.sect{font-size:1.16rem;font-weight:760;color:#f0f8fb;margin:18px 0 13px}
.label-block{font-size:.86rem;color:var(--sb-gold);font-weight:750}
.small{font-size:.88rem;color:#c1d4de;line-height:1.7}
.foot{border-top:1px solid #355365;margin-top:30px;padding-top:18px;
  color:#bbceda;font-size:.83rem;line-height:1.65}
@keyframes sb-intro{
  from{opacity:.35;transform:translateY(-16px) scale(.96)}
  to{opacity:1;transform:none}
}
:focus-visible{outline:3px solid #f5d6a7!important;outline-offset:3px}
@media(max-width:880px){
  [data-testid="stMainBlockContainer"],.block-container {padding-top:.8rem}
  [data-testid="stMetric"]{min-height:109px;padding:13px 14px}
  [data-testid="stMetricValue"]{font-size:1.38rem}
  .sb-hero{padding:26px}
}
@media(max-width:620px){
  .sb-hero{padding:23px;border-radius:18px}
  .sb-hero h1{font-size:2.15rem}
  .sb-hero:after{width:195px;right:-115px;top:-100px}
  .sb-context{gap:6px;padding:9px}
  .sb-chip{font-size:.74rem}
  [data-testid="stPlotlyChart"]{padding:0;border-radius:12px}
  [data-testid="stMetric"]{min-height:98px}
}
@media(prefers-reduced-motion:reduce){
  *,*:before,*:after{animation:none!important;transition:none!important;
    scroll-behavior:auto!important}
}

/* Subtle interaction feedback, respecting system reduced-motion preferences. */
@media (prefers-reduced-motion: no-preference) {
  [data-testid="stMainBlockContainer"] {animation:sb-page-enter .38s ease-out both}
  [data-testid="stMetric"], [data-testid="stPlotlyChart"],
  [data-testid="stVerticalBlockBorderWrapper"], [data-testid="stAlert"],
  [data-testid="stLinkButton"] a, [data-testid="stSidebarNav"] a {
    transition:transform .28s cubic-bezier(.2,.8,.2,1), border-color .25s ease,
               box-shadow .3s ease, background-color .25s ease;
  }
  [data-testid="stMetric"]:hover {transform:translateY(-4px) scale(1.018);
    border-color:#65aeb2;box-shadow:0 18px 35px -24px #000}
  [data-testid="stPlotlyChart"]:hover {transform:translateY(-2px) scale(1.008);
    border-color:#507e8a}
  [data-testid="stLinkButton"] a:hover {transform:translateY(-2px) scale(1.015)}
  [data-testid="stTabs"] button[role="tab"] {transition:color .24s ease,background .24s ease,transform .24s ease}
  [data-testid="stTabs"] button[role="tab"]:hover {transform:translateY(-2px);background:rgba(104,229,207,.08)}
  [data-testid="stSidebarNav"] a:hover {transform:translateX(3px)}
  .sb-hero {animation:sb-page-enter .5s ease-out both}
}
@keyframes sb-page-enter {from {opacity:.2;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
[data-testid="stLinkButton"] a[href*="github.com"] {
 background:linear-gradient(110deg,#152936,#203a4c)!important;
 border:1px solid #426a7c!important;color:#eaf8fb!important;
}
[data-testid="stLinkButton"] a[href*="github.com"]:before {
 content:"";display:inline-block;width:17px;height:17px;margin-right:8px;
 vertical-align:-3px;
 background-color:currentColor;
 -webkit-mask:url("data:image/svg+xml,%3Csvg viewBox='0 0 24 24' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M12 .7a11.3 11.3 0 0 0-3.57 22.02c.56.1.77-.24.77-.54v-2.08c-3.12.68-3.78-1.33-3.78-1.33-.5-1.28-1.24-1.62-1.24-1.62-1.02-.7.08-.69.08-.69 1.13.08 1.72 1.16 1.72 1.16 1 .1.86 1.73 3.25 1.23.1-.73.4-1.23.72-1.51-2.49-.29-5.11-1.24-5.11-5.56 0-1.23.44-2.23 1.16-3.02-.12-.28-.5-1.44.11-2.99 0 0 .95-.3 3.11 1.15a10.9 10.9 0 0 1 5.67 0c2.16-1.46 3.11-1.15 3.11-1.15.61 1.55.23 2.71.11 2.99.73.79 1.16 1.79 1.16 3.02 0 4.33-2.63 5.27-5.13 5.55.41.36.78 1.05.78 2.11v3.12c0 .3.2.65.78.54A11.3 11.3 0 0 0 12 .7Z'/%3E%3C/svg%3E") center/contain no-repeat;
 mask:url("data:image/svg+xml,%3Csvg viewBox='0 0 24 24' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M12 .7a11.3 11.3 0 0 0-3.57 22.02c.56.1.77-.24.77-.54v-2.08c-3.12.68-3.78-1.33-3.78-1.33-.5-1.28-1.24-1.28-1.24-1.28-1.02-.7.08-.69.08-.69 1.13.08 1.72 1.16 1.72 1.16 1 .1.86 1.73 3.25 1.23.1-.73.4-1.23.72-1.51-2.49-.29-5.11-1.24-5.11-5.56 0-1.23.44-2.23 1.16-3.02-.12-.28-.5-1.44.11-2.99 0 0 .95-.3 3.11 1.15a10.9 10.9 0 0 1 5.67 0c2.16-1.46 3.11-1.15 3.11-1.15.61 1.55.23 2.71.11 2.99.73.79 1.16 1.79 1.16 3.02 0 4.33-2.63 5.27-5.13 5.55.41.36.78 1.05.78 2.11v3.12c0 .3.2.65.78.54A11.3 11.3 0 0 0 12 .7Z'/%3E%3C/svg%3E") center/contain no-repeat;
}
</style>
"""


def inject() -> None:
    """Add constant, sanitizer-compatible CSS without enabling JavaScript."""
    st.html(CSS)


def hero(kicker: str, title: str, description: str) -> None:
    """Accessible static HTML header with escaped dynamic text."""
    st.html(
        '<section class="sb-hero" aria-label="Page introduction">'
        f'<span class="sb-eyebrow">{escape(kicker)}</span>'
        f'<h1>{escape(title)}</h1>'
        f'<p>{escape(description)}</p></section>'
    )


def section_intro(label: str) -> None:
    st.html(f'<div class="sb-section-intro">{escape(label)}</div>')


def note(text: str) -> None:
    st.html(f'<div class="sb-note">{escape(text)}</div>')


def footer() -> None:
    st.html(
        '<footer class="sb-footer">'
        '<strong>Sand Battery Studio · Group 8</strong> — Numerical research '
        'platform. Not experimentally validated or construction-certified. '
        '<a href="https://github.com/bysquizy/Sand-Battery-Project" '
        'target="_blank" rel="noopener noreferrer">Source code & methods</a>.'
        '</footer>'
    )
