import streamlit as st
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['figure.facecolor'] = '#ffffff'
matplotlib.rcParams['axes.facecolor'] = '#f8fafc'
matplotlib.rcParams['axes.spines.top'] = False
matplotlib.rcParams['axes.spines.right'] = False
import io

def pdf_rapor_olustur(tahmin, model, urun_adi, siparis, siradaki, guvenlik, tedarik):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    import io
    import matplotlib.pyplot as plt
    import datetime

    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
        rightMargin=2*cm, leftMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm)

    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    pass  # built-in font kullanılıyor

    styles = getSampleStyleSheet()
    story = []

    # Başlık
    baslik_style = ParagraphStyle('baslik', fontSize=20, fontName='Helvetica',
        textColor=colors.HexColor('#0f1f3d'), spaceAfter=6, alignment=TA_CENTER)
    alt_style = ParagraphStyle('alt', fontSize=11, fontName='Helvetica',
        textColor=colors.HexColor('#64748b'), spaceAfter=20, alignment=TA_CENTER)
    normal = ParagraphStyle('normal', fontSize=10, fontName='Helvetica',
        textColor=colors.HexColor('#2d3748'), spaceAfter=6)

    story.append(Paragraph("Talep Tahmin Raporu", baslik_style))
    story.append(Paragraph(f"Kobi Start — {datetime.datetime.now().strftime('%d.%m.%Y %H:%M')}", alt_style))
    story.append(Spacer(1, 0.3*cm))

    # Özet tablo
    tablo_data = [
        ['Parametre', 'Değer'],
        ['Ürün / Veri', str(urun_adi)],
        [f'Tahmini Satış ({tedarik} gün)', f'{round(siradaki):,} adet'],
        ['Önerilen Sipariş Miktarı', f'{siparis:,} adet'],
        ['Güvenlik Stoğu', f'{guvenlik} adet'],
        ['Tedarik Süresi', f'{tedarik} gün'],
    ]

    tablo = Table(tablo_data, colWidths=[8*cm, 8*cm])
    tablo.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f1f3d')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#f8fafc'), colors.white]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 8),
        ('ALIGN', (1,0), (1,-1), 'CENTER'),
    ]))
    story.append(tablo)
    story.append(Spacer(1, 0.5*cm))

    # Grafik
    story.append(Paragraph("Satış Tahmini Grafiği", ParagraphStyle('h2',
        fontSize=13, fontName='Helvetica',
        textColor=colors.HexColor('#0f1f3d'), spaceAfter=8)))

    fig, ax = plt.subplots(figsize=(14, 4))
    model.plot(tahmin, ax=ax)
    ax.set_title("")
    ax.set_xlabel("Tarih")
    ax.set_ylabel("Satış")
    fig.tight_layout()

    img_buf = io.BytesIO()
    fig.savefig(img_buf, format='png', dpi=150, bbox_inches='tight')
    img_buf.seek(0)
    plt.close(fig)

    story.append(Image(img_buf, width=16*cm, height=5*cm))
    story.append(Spacer(1, 0.5*cm))

    # Mevsimsellik
    story.append(Paragraph("Mevsimsellik Analizi", ParagraphStyle('h2',
        fontSize=13, fontName='Helvetica',
        textColor=colors.HexColor('#0f1f3d'), spaceAfter=8)))

    fig2 = model.plot_components(tahmin)
    fig2.set_size_inches(14, 6)
    img_buf2 = io.BytesIO()
    fig2.savefig(img_buf2, format='png', dpi=150, bbox_inches='tight')
    img_buf2.seek(0)
    plt.close(fig2)

    story.append(Image(img_buf2, width=16*cm, height=6*cm))

    doc.build(story)
    buf.seek(0)
    return buf


st.set_page_config(
    page_title="KOBİ Start — Talep Tahmin",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Serif+Display&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background-color: #f0f2f6;
}

section[data-testid="stSidebar"] {
    background-color: #0f1f3d;
    border-right: none;
}

section[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}

section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stSlider label,
section[data-testid="stSidebar"] .stNumberInput label,
section[data-testid="stSidebar"] .stFileUploader label {
    color: #94a3b8 !important;
    font-size: 12px !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 500;
}

section[data-testid="stSidebar"] .stButton>button {
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    color: white !important;
    border: none;
    border-radius: 8px;
    padding: 12px 0;
    font-size: 14px;
    font-weight: 600;
    width: 100%;
    letter-spacing: 0.03em;
    transition: all 0.2s;
    margin-top: 8px;
}

section[data-testid="stSidebar"] .stButton>button:hover {
    background: linear-gradient(135deg, #1d4ed8, #1e40af);
    transform: translateY(-1px);
}

.sidebar-logo {
    padding: 24px 0 32px 0;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 24px;
}

.sidebar-section {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.12em;
    color: #475569 !important;
    text-transform: uppercase;
    margin: 24px 0 8px 0;
}

.main-header {
    background: linear-gradient(135deg, #0f1f3d 0%, #1e3a6e 100%);
    border-radius: 16px;
    padding: 36px 40px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.header-title {
    font-family: 'DM Serif Display', serif;
    font-size: 28px;
    font-weight: 400;
    color: white;
    margin: 0;
    line-height: 1.2;
}

.header-sub {
    font-size: 14px;
    color: #94a3b8;
    margin-top: 6px;
    font-weight: 300;
}

.header-badge {
    background: rgba(37,99,235,0.3);
    border: 1px solid rgba(37,99,235,0.5);
    color: #93c5fd;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 500;
    letter-spacing: 0.05em;
}

.card {
    background: white;
    border-radius: 12px;
    padding: 24px;
    border: 1px solid #e2e8f0;
    margin-bottom: 16px;
}

.card-title {
    font-size: 13px;
    font-weight: 600;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 16px;
}

.metric-row {
    display: flex;
    gap: 16px;
    margin-bottom: 16px;
}

.metric-box {
    flex: 1;
    background: #f8fafc;
    border-radius: 10px;
    padding: 16px 20px;
    border: 1px solid #e2e8f0;
}

.metric-label {
    font-size: 11px;
    color: #94a3b8;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 6px;
}

.metric-value {
    font-size: 28px;
    font-weight: 600;
    color: #0f1f3d;
    line-height: 1;
}

.metric-unit {
    font-size: 13px;
    color: #64748b;
    margin-left: 4px;
}

.metric-box.highlight {
    background: #0f1f3d;
    border-color: #0f1f3d;
}

.metric-box.highlight .metric-label { color: #64748b; }
.metric-box.highlight .metric-value { color: white; }
.metric-box.highlight .metric-unit { color: #94a3b8; }

.empty-state {
    text-align: center;
    padding: 80px 40px;
    background: white;
    border-radius: 16px;
    border: 2px dashed #e2e8f0;
}

.empty-icon { font-size: 48px; margin-bottom: 16px; }
.empty-title { font-size: 20px; font-weight: 600; color: #0f1f3d; margin-bottom: 8px; }
.empty-sub { font-size: 14px; color: #94a3b8; }

div[data-testid="stMetric"] {
    background: white;
    border-radius: 10px;
    padding: 16px 20px;
    border: 1px solid #e2e8f0;
}

.stTabs [data-baseweb="tab-list"] {
    background: white;
    border-radius: 10px;
    padding: 4px;
    border: 1px solid #e2e8f0;
    gap: 4px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    font-size: 13px;
    font-weight: 500;
    color: #64748b;
}

.stTabs [aria-selected="true"] {
    background: #0f1f3d !important;
    color: white !important;
}

hr { border-color: #e2e8f0; }
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div style="font-size:22px;font-weight:700;color:white;letter-spacing:-0.5px;">📦 KOBİ Start</div>
        <div style="font-size:11px;color:#475569;margin-top:4px;letter-spacing:0.05em;">TALEP TAHMİN SİSTEMİ</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">Veri Yükle</div>', unsafe_allow_html=True)
    dosya = st.file_uploader("CSV veya Excel", type=["csv", "xlsx", "xls"], label_visibility="collapsed")

    if dosya:
        if dosya.name.endswith(".csv"):
            try:
                df = pd.read_csv(dosya, encoding="latin1")
            except:
                df = pd.read_csv(dosya, encoding="utf-8")
        else:
            df = pd.read_excel(dosya)

        st.success(f"✓  {len(df):,} satır yüklendi")

        st.markdown('<div class="sidebar-section">Kolonlar</div>', unsafe_allow_html=True)
        tarih_kolon = st.selectbox("Tarih", df.columns)
        satis_kolon = st.selectbox("Satış", df.columns)
        urun_kolon = st.selectbox("Ürün (opsiyonel)", ["— Yok —"] + list(df.columns))

        st.markdown('<div class="sidebar-section">Parametreler</div>', unsafe_allow_html=True)
        tahmin_gun = st.slider("Tahmin süresi (gün)", 30, 180, 90)
        tedarik = st.slider("Tedarik süresi (gün)", 7, 60, 14)
        guvenlik = st.number_input("Güvenlik stoğu", value=20, min_value=0)
        mevcut = st.number_input("Mevcut stok", value=0, min_value=0)

        tahmin_btn = st.button("Tahmin Et →")
    else:
        tahmin_btn = False
        df = None

# ── MAIN ──
st.markdown("""
<div class="main-header">
    <div>
        <div class="header-title">Talep Tahmin &<br>Sipariş Optimizasyonu</div>
        <div class="header-sub">Geçmiş satışlarınızı yükleyin, yapay zeka ile optimize edin.</div>
    </div>
    <div class="header-badge">AI Destekli · Prophet Model</div>
</div>
""", unsafe_allow_html=True)

def tahmin_yap(veri, tarih, satis, gun):
    gunluk = veri.groupby(tarih)[satis].sum().reset_index()
    gunluk.columns = ["ds", "y"]
    gunluk = gunluk[gunluk["y"] > 0]
    model = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False)
    model.fit(gunluk)
    gelecek = model.make_future_dataframe(periods=gun)
    return model, model.predict(gelecek)

def ciz(model, tahmin, baslik):
    fig, ax = plt.subplots(figsize=(11, 3.5))
    model.plot(tahmin, ax=ax)
    ax.set_title(baslik, fontsize=13, fontweight='600', color='#0f1f3d', pad=12)
    ax.set_xlabel("Tarih", fontsize=11, color='#64748b')
    ax.set_ylabel("Satış", fontsize=11, color='#64748b')
    ax.tick_params(colors='#94a3b8', labelsize=9)
    fig.tight_layout()
    return fig

if not dosya:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">📂</div>
        <div class="empty-title">Başlamak için veri yükleyin</div>
        <div class="empty-sub">Sol panelden CSV veya Excel dosyanızı yükleyin.<br>Geçmiş satış verilerinizle anlık tahmin alın.</div>
    </div>
    """, unsafe_allow_html=True)

elif dosya and tahmin_btn:
    df[tarih_kolon] = pd.to_datetime(df[tarih_kolon], dayfirst=True, errors="coerce")
    df = df.dropna(subset=[tarih_kolon])

    if urun_kolon != "— Yok —":
        urunler = list(df[urun_kolon].unique()[:5])
        secili = st.multiselect("Karşılaştırılacak ürünler", urunler, default=urunler[:2])
        tab_labels = secili + ["Mevsimsellik"]
        tabs = st.tabs(tab_labels)

        for i, urun in enumerate(secili):
            with tabs[i]:
                urun_df = df[df[urun_kolon] == urun]
                with st.spinner(f"{urun} hesaplanıyor..."):
                    model, tahmin = tahmin_yap(urun_df, tarih_kolon, satis_kolon, tahmin_gun)

                siradaki = tahmin.tail(tedarik)["yhat"].sum()
                siparis = max(0, round(siradaki + guvenlik - mevcut))

                st.markdown(f"""
                <div class="metric-row">
                    <div class="metric-box">
                        <div class="metric-label">Tahmini satış ({tedarik} gün)</div>
                        <div class="metric-value">{round(siradaki):,}<span class="metric-unit">adet</span></div>
                    </div>
                    <div class="metric-box highlight">
                        <div class="metric-label">Önerilen sipariş</div>
                        <div class="metric-value">{siparis:,}<span class="metric-unit">adet</span></div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-label">Güvenlik stoğu</div>
                        <div class="metric-value">{guvenlik}<span class="metric-unit">adet</span></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                fig = ciz(model, tahmin, f"{urun} — {tahmin_gun} Günlük Tahmin")
                st.pyplot(fig)
                buf = io.BytesIO()
                fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
                st.download_button(f"⬇️ Grafiği indir", buf.getvalue(), f"{urun}_tahmin.png", "image/png")

        with tabs[-1]:
            urun_df = df[df[urun_kolon] == secili[0]] if secili else df
            with st.spinner("Mevsimsellik analizi..."):
                model, tahmin = tahmin_yap(urun_df, tarih_kolon, satis_kolon, tahmin_gun)
            fig2 = model.plot_components(tahmin)
            fig2.set_size_inches(11, 6)
            st.pyplot(fig2)
            buf2 = io.BytesIO()
            fig2.savefig(buf2, format="png", dpi=150, bbox_inches="tight")
            st.download_button("⬇️ Mevsimsellik grafiğini indir", buf2.getvalue(), "mevsimsellik.png", "image/png")
    else:
        with st.spinner("Model kuruluyor..."):
            model, tahmin = tahmin_yap(df, tarih_kolon, satis_kolon, tahmin_gun)

        siradaki = tahmin.tail(tedarik)["yhat"].sum()
        siparis = max(0, round(siradaki + guvenlik - mevcut))

        st.markdown(f"""
        <div class="metric-row">
            <div class="metric-box">
                <div class="metric-label">Tahmini satış ({tedarik} gün)</div>
                <div class="metric-value">{round(siradaki):,}<span class="metric-unit">adet</span></div>
            </div>
            <div class="metric-box highlight">
                <div class="metric-label">Önerilen sipariş</div>
                <div class="metric-value">{siparis:,}<span class="metric-unit">adet</span></div>
            </div>
            <div class="metric-box">
                <div class="metric-label">Güvenlik stoğu</div>
                <div class="metric-value">{guvenlik}<span class="metric-unit">adet</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["Tahmin Grafiği", "Mevsimsellik Analizi"])
        with tab1:
            fig = ciz(model, tahmin, f"{tahmin_gun} Günlük Satış Tahmini")
            st.pyplot(fig)
            buf = io.BytesIO()
            fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
            st.download_button("⬇️ Grafiği indir", buf.getvalue(), "tahmin.png", "image/png")
            pdf_buf = pdf_rapor_olustur(tahmin, model, "Genel", siparis, siradaki, guvenlik, tedarik)
            st.download_button("📄 PDF Rapor İndir", pdf_buf.getvalue(), "tahmin_raporu.pdf", "application/pdf")
        with tab2:
            fig2 = model.plot_components(tahmin)
            fig2.set_size_inches(11, 6)
            st.pyplot(fig2)

elif dosya and not tahmin_btn:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">⚙️</div>
        <div class="empty-title">Parametreleri ayarlayın</div>
        <div class="empty-sub">Sol panelden kolonları ve parametreleri seçin,<br>ardından <b>Tahmin Et</b> butonuna basın.</div>
    </div>
    """, unsafe_allow_html=True)

