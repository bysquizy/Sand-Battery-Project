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
    return st.session_state.get("sb_language", "en")
def t(key):
    return TEXT[language()].get(key, TEXT["en"].get(key, key))
def tr(en, turkish):
    return turkish if language()=="tr" else en
