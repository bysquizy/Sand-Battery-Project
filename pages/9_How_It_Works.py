"""Bilingual guide to the educational thermal-storage model."""
import streamlit as st
from localization import t, tr
from ui_theme import inject, hero, footer
from project_info import PROJECT

st.set_page_config(page_title="How It Works | Sand Battery",page_icon="❔",layout="wide")
inject()
hero(tr("PROJECT GUIDE", "PROJE REHBERİ"),t("how_intro"),t("how_sub"))
st.info(tr("This is a numerical educational model, not a tested physical installation.",
           "Bu bir eğitim amaçlı sayısal modeldir; gerçek bir tesiste deneysel olarak doğrulanmamıştır."))

a,b,c=st.columns(3)
with a:
    with st.container(border=True):
        st.markdown("### 🔌 "+t("charge"))
        st.write(tr("Electrical input or a configured solar-thermal input heats the storage medium. Charging power, input efficiency and target temperature matter.",
                    "Elektrik enerjisi veya seçilen güneş kaynaklı ısı girişi depolama malzemesini ısıtır. Şarj gücü, giriş verimi ve hedef sıcaklık önemlidir."))
with b:
    with st.container(border=True):
        st.markdown("### 🌡️ "+t("store"))
        st.write(tr("Energy is retained as sensible heat. Insulation, ambient temperature, storage duration and tank dimensions influence losses.",
                    "Enerji duyulur ısı olarak depolanır. Yalıtım, ortam sıcaklığı, bekleme süresi ve depo boyutları ısı kaybını etkiler."))
with c:
    with st.container(border=True):
        st.markdown("### ♨️ "+t("discharge"))
        st.write(tr("The model estimates how much useful heat can be taken from the store. This is thermal output, not electricity produced.",
                    "Model depodan ne kadar kullanılabilir ısı çekilebileceğini hesaplar. Bu ısı enerjisidir; üretilen elektrik değildir."))

st.markdown(tr("## Try a simple calculation","## Basit bir hesap deneyin"))
col1,col2,col3=st.columns(3)
with col1: mass=st.slider(tr("Material mass (kg)","Malzeme kütlesi (kg)"),100,10000,1000,100)
with col2: temp=st.slider(tr("Hot temperature (°C)","Yüksek sıcaklık (°C)"),150,600,500,10)
with col3: low=st.slider(tr("Reference temperature (°C)","Referans sıcaklık (°C)"),20,min(temp-10,300),100,10)
q=mass*830*(temp-low)/3_600_000_000
st.metric(tr("Theoretical thermal energy (MWh)","Teorik ısı enerjisi (MWh)"),f"{q:.3f}")
st.latex(r"Q=m\,c_p\,\Delta T")
st.caption(tr("Demonstration assumes a constant heat capacity of 830 J/(kg·K) and ignores heat loss. The application's engineering pages use additional assumptions and models.",
              "Bu örnekte özgül ısı 830 J/(kg·K) sabit kabul edilir ve ısı kaybı ihmal edilir. Uygulamanın mühendislik sayfalarında daha ayrıntılı modeller ve varsayımlar kullanılır."))

st.markdown(tr("## Using the application","## Uygulamanın kullanımı"))
for title_en,title_tr,body_en,body_tr in [
("1. Configure the model","1. Modeli ayarlayın","Use the shared sidebar editor to choose material, geometry, temperature limits and energy inputs.","Yan menüden malzeme, geometri, sıcaklık sınırları ve enerji girdilerini seçin."),
("2. Run the dashboard","2. Simülasyonu inceleyin","Review stored energy, useful heat, calculated losses and temperature plots.","Depolanan enerjiyi, kullanılabilir ısıyı, hesaplanan kayıpları ve sıcaklık grafiklerini inceleyin."),
("3. Compare designs","3. Tasarımları karşılaştırın","Save scenarios and vary the insulation, mass and operating assumptions.","Senaryoları kaydedin; yalıtım, kütle ve çalışma varsayımlarını değiştirin."),
("4. Examine limitations","4. Modelin sınırlarını inceleyin","Use Model Verification and Research Hub to check equations, references and evidence.","Model Doğrulama ve Araştırma Merkezi sayfalarında denklemleri, kaynakları ve kanıtları kontrol edin.")
]:
    with st.expander(tr(title_en,title_tr)):
        st.write(tr(body_en,body_tr))
st.link_button(tr("View source code on GitHub","GitHub'da kaynak kodunu aç"),PROJECT["repository"])
st.caption(t("author"))
footer()
