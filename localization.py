"""Shared Turkish/English strings for the student project."""
import streamlit as st

TEXT = {
 "en": {
 "language":"Language / Dil", "simulation":"Simulation", "research":"Research & Sources",
 "advanced":"Advanced Research", "dashboard":"Engineering Dashboard",
 "design":"Thermal Design Studio", "scenarios":"Scenario Manager",
 "verification":"Model Verification", "visuals":"Visual Story Studio",
 "laboratory":"Advanced Research Lab", "materials":"Material Atlas",
 "experiments":"Virtual Experiments", "research_hub":"Research Hub",
 "how":"How It Works", "sidebar_project":"GROUP 8 · STUDENT PROJECT",
 "intro":"Thermal energy storage simulation", "active":"Active model",
 "pages":"Pages and functions", "github":"GitHub project repository",
 "live":"Open the simulation", "author":"Website development: Yağız Topaç (@bysquizy) · Team: Yağız Topaç, Semih Cenk, Fatma Ovacık",
 "how_intro":"How the sand-battery simulation works", "how_sub":"A guided explanation of the energy pathway, controls and results.",
 "charge":"1 · Charge", "store":"2 · Store", "discharge":"3 · Deliver heat",
 },
 "tr": {
 "language":"Dil / Language", "simulation":"Simülasyon", "research":"Araştırma ve Kaynaklar",
 "advanced":"İleri Araştırma", "dashboard":"Mühendislik Paneli",
 "design":"Termal Tasarım", "scenarios":"Senaryo Yöneticisi",
 "verification":"Model Doğrulama", "visuals":"Görsel Analiz",
 "laboratory":"İleri Araştırma Laboratuvarı", "materials":"Malzeme Atlası",
 "experiments":"Sanal Deneyler", "research_hub":"Araştırma Merkezi",
 "how":"Nasıl Çalışır?", "sidebar_project":"GRUP 8 · ÖĞRENCİ PROJESİ",
 "intro":"Termal enerji depolama simülasyonu", "active":"Aktif model",
 "pages":"Sayfalar ve işlevler", "github":"GitHub proje deposu",
 "live":"Simülasyonu aç", "author":"Web sitesi: Yağız Topaç (@bysquizy) · Ekip: Yağız Topaç, Semih Cenk, Fatma Ovacık",
 "how_intro":"Kum bataryası simülasyonu nasıl çalışır?", "how_sub":"Enerji akışını, ayarları ve sonuçları adım adım keşfedin.",
 "charge":"1 · Şarj", "store":"2 · Depola", "discharge":"3 · Isıyı kullan",
 }
}
def language():
    selected = st.session_state.get("sb_language", "en")
    return selected if selected in TEXT else "en"
def t(key):
    return TEXT[language()].get(key, TEXT["en"].get(key, key))
def tr(en, turkish):
    return turkish if language()=="tr" else en


# Display-only mappings: saved JSON, model keys and source identifiers stay English.
SOURCE_TR = {
    "Electric heater": "Elektrikli ısıtıcı",
    "CSP thermal": "Yoğunlaştırılmış güneş ısısı",
    "PV + wind": "Güneş PV + rüzgâr",
}
MATERIAL_TR = {
    "Silica sand": "Silis kumu",
    "Crushed basalt": "Kırılmış bazalt",
    "Crushed refractory brick": "Kırılmış refrakter tuğla",
    "Crushed soapstone (illustrative)": "Kırılmış sabuntaşı (temsili)",
    "Industrial by-product (illustrative)": "Endüstriyel yan ürün (temsili)",
}
PRESET_TR = {
    "Industrial thermal store": "Endüstriyel ısı deposu",
    "Compact research study": "Kompakt araştırma örneği",
    "CSP-assisted thermal storage": "CSP destekli ısı depolama",
}


def source_label(value: str) -> str:
    return tr(value, SOURCE_TR.get(value, value))


def material_label(value: str) -> str:
    return tr(value, MATERIAL_TR.get(value, value))


def preset_label(value: str) -> str:
    return tr(value, PRESET_TR.get(value, value))


def material_option_label(value: str) -> str:
    """Stable bilingual option: language switches cannot invalidate widget state."""
    translated = MATERIAL_TR.get(value)
    return f"{value} / {translated}" if translated else value


def source_option_label(value: str) -> str:
    translated = SOURCE_TR.get(value)
    return f"{value} / {translated}" if translated else value


def preset_option_label(value: str) -> str:
    translated = PRESET_TR.get(value)
    return f"{value} / {translated}" if translated else value
