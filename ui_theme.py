"""Shared web styling adapted from the team-supplied ui_theme.py.

Presentation only: no engineering formulas, external fonts or network requests.
Reduced-motion preference, keyboard focus and mobile layouts are respected.
"""
import streamlit as st

CSS = """
<style>
:root{--copper:#eeb37e;--copper-2:#df9874;--mint:#58dfc3;--ink:#08111d;--panel:#0f1d2a;--line:#283d4c;--muted:#a7bdcb}
.stApp{
 background:radial-gradient(ellipse 900px 460px at 78% -180px,rgba(45,124,145,.19),transparent 80%),
 radial-gradient(ellipse 700px 380px at -8% 12%,rgba(238,179,126,.08),transparent 75%),#08111d;color:#e7eff5}
html,body,[class*='css']{font-family:system-ui,'Segoe UI',sans-serif}
[data-testid='stMainBlockContainer'],.block-container{max-width:1480px;padding-top:1.25rem;padding-bottom:3.5rem}
[data-testid='stSidebar']{background:linear-gradient(180deg,#0d1b28,#091521);border-right:1px solid var(--line)}
[data-testid='stSidebar'] summary{font-weight:700;letter-spacing:.04em}
[data-testid='stMetric']{
 background:linear-gradient(135deg,#203443e9,#0e1d2bfa);border:1px solid var(--line);border-radius:16px;
 padding:16px 18px;min-height:106px;box-shadow:0 12px 24px -20px #000;
 transition:transform .24s ease,border-color .24s ease}
[data-testid='stMetric']:hover{transform:translateY(-2px);border-color:var(--copper-2)}
[data-testid='stMetricLabel'] p{font-size:.78rem;color:#b3c7d4;letter-spacing:.025em;font-weight:600}
[data-testid='stMetricValue']{font-size:1.6rem;font-weight:780;color:#f4f8fa}
[data-testid='stPlotlyChart']{
 border:1px solid #2a4655;border-radius:15px;background:linear-gradient(145deg,#132434,#0c1826);
 padding:3px;transition:border-color .2s ease}
[data-testid='stPlotlyChart']:hover{border-color:#5f8a95}
[data-testid='stDataFrame']{border:1px solid var(--line);border-radius:11px}
div[data-testid='stExpander']{border:1px solid var(--line);border-radius:12px;background:#12202d9f}
div[data-testid='stAlert']{border-radius:11px}
.stButton button,.stDownloadButton button{border-radius:11px;font-weight:700;transition:transform .2s ease,box-shadow .2s ease}
.stButton button:hover,.stDownloadButton button:hover{transform:translateY(-1px)}
.stButton button[kind='primary']{background:linear-gradient(110deg,#f2c48e,#df9874);color:#091522;font-weight:800}
.stDownloadButton button{border:1px solid #476575}
div[data-testid='stTabs'] button[role='tab']{font-weight:700;color:#b1c5d1}
div[data-testid='stTabs'] button[aria-selected='true']{color:var(--copper)}
div[data-testid='stTabs'] [data-baseweb='tab-highlight']{background:var(--copper);height:3px}
.hero{position:relative;overflow:hidden;border:1px solid #35505e;border-radius:22px;padding:30px 34px;margin:4px 0 24px;
 background:linear-gradient(110deg,#163343 0%,#102430 55%,#242c35 100%);box-shadow:0 20px 35px -32px #000;
 animation:ui-rise .65s ease-out both}
.hero:before{content:'';position:absolute;inset:0;pointer-events:none;
 background:linear-gradient(110deg,transparent 30%,#ffffff0a 50%,transparent 70%);
 background-size:250% 100%;animation:ui-shimmer 9s ease-in-out infinite}
.hero:after{content:'';position:absolute;width:420px;height:420px;border-radius:50%;right:-130px;top:-235px;
 border:52px solid #eeb37e18;animation:ui-orbit 15s ease-in-out infinite alternate;pointer-events:none}
.hero h1{font-size:clamp(1.65rem,3.4vw,2.65rem);font-weight:800;letter-spacing:-.045em;color:#f3f9fc;margin:.5rem 0}
.hero p{color:#b9cdd8;max-width:740px;font-size:.95rem;line-height:1.75;margin:0}
.eyebrow{font-size:.7rem;letter-spacing:.18em;text-transform:uppercase;color:#83ead7;font-weight:800}
.pill{display:inline-flex;padding:5px 10px;color:#b2fae8;border:1px solid #438e85;background:#133c38;border-radius:20px}
.info-line{border-left:3px solid var(--copper);background:#142938;border-radius:0 10px 10px 0;
 padding:12px 16px;color:#bdd1dc;font-size:.89rem;margin:12px 0}
.sect{font-size:1.13rem;font-weight:800;color:#ecf4f7;margin:16px 0 12px}
.label-block{color:var(--copper);font-weight:800;font-size:.8rem;text-transform:uppercase;letter-spacing:.09em}
.small{font-size:.82rem;color:#aec2cc;line-height:1.6}
.foot{border-top:1px solid var(--line);margin-top:28px;padding-top:16px;color:#a4bcc9;font-size:.8rem;line-height:1.8}
h1,h2,h3{letter-spacing:-.025em}
:focus-visible{outline:3px solid #f4c796!important;outline-offset:3px}
@keyframes ui-rise{from{opacity:.4;transform:translateY(9px)}to{opacity:1;transform:none}}
@keyframes ui-shimmer{0%,65%{background-position:140% 0}100%{background-position:-140% 0}}
@keyframes ui-orbit{to{transform:translate(-36px,52px) rotate(38deg)}}
@media(max-width:900px){[data-testid='stMetricValue']{font-size:1.3rem}}
@media(max-width:680px){.hero{padding:20px}.hero:after,.hero:before{display:none}
 [data-testid='stMetric']{min-height:95px;padding:11px}}
@media(prefers-reduced-motion:reduce){*,*:before,*:after{
 animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important}}
</style>
"""

def inject() -> None:
    """Apply the shared lightweight theme once per page, after page configuration."""
    st.markdown(CSS, unsafe_allow_html=True)
