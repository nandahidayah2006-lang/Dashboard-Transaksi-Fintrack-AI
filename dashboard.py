import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# =========================================================================
# 1. KONFIGURASI HALAMAN & THEME PREMIUM (ALA ASISTEN KEUANGAN MODERN)
# =========================================================================
st.set_page_config(
    page_title="Fintrack AI",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk menyulap UI Streamlit menjadi sekelas aplikasi perbankan modern
st.markdown("""
    <style>
    /* Mengubah background utama */
    .stApp { background-color: #F8FAFC; }
    
    /* Styling Card Metric */
    div[data-testid="metric-container"] {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        padding: 20px 25px;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        transition: transform 0.2s ease-in-out;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-4px);
        border-color: #CBD5E1;
    }
    div[data-testid="stMetricLabel"] > div {
        font-size: 14px !important;
        font-weight: 600 !important;
        color: #64748B !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    div[data-testid="stMetricValue"] > div {
        font-size: 26px !important;
        font-weight: 700 !important;
        color: #0F172A !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Custom Tab Styling */
    button[data-baseweb="tab"] {
        font-size: 16px !important;
        font-weight: 600 !important;
        padding: 12px 24px !important;
    }
    
    /* Info text */
    .insight-box {
        background-color: #F0FDF4;
        border-left: 5px solid #16A34A;
        padding: 15px;
        border-radius: 8px;
        color: #166534;
        font-size: 14px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# =========================================================================
# 2. MEKANISME RETRIEVAL DATA KLASTER (MENGUTAMAKAN FILE TERBARU)
# =========================================================================
@st.cache_data
def load_financial_data():
    # Mengutamakan file hasil clustering yang baru Abang buat
    target_files = ["DATASET_KEUANGAN_CLUSTERED.xlsx", "DATASET_KEUANGAN_UPDATED.xlsx", "DATASET_KEUANGAN_FINAL_FIXED.xlsx"]
    df = None
    
    for file_name in target_files:
        if os.path.exists(file_name):
            try:
                df = pd.read_excel(file_name, engine="openpyxl")
                break
            except Exception:
                continue
                
    if df is None:
        # Fallback dummy jika file tidak sengaja hilang
        dates = pd.date_range(start="2022-01-01", end="2026-12-31", freq="D")
        np.random.seed(42)
        dummy_data = {
            'tanggal': dates,
            'tipe_label': np.random.choice(['Uang Masuk', 'Uang Keluar'], size=len(dates), p=[0.1, 0.9]),
            'nama_kategori_label': np.random.choice(['Keinginan', 'Kebutuhan', 'Tabungan'], size=len(dates), p=[0.5, 0.4, 0.1]),
            'jumlah': np.random.exponential(scale=100000, size=len(dates)).astype(int),
            'status_label': np.random.choice(['Boros', 'Hemat'], size=len(dates), p=[0.4, 0.6])
        }
        df = pd.DataFrame(dummy_data)
        df.loc[df['tipe_label'] == 'Uang Masuk', 'jumlah'] = np.random.randint(12000000, 15000000, size=len(df[df['tipe_label'] == 'Uang Masuk']))
        df.loc[df['tipe_label'] == 'Uang Keluar', 'jumlah'] = np.random.randint(20000, 150000, size=len(df[df['tipe_label'] == 'Uang Keluar']))
        df['tipe'] = np.where(df['tipe_label'] == 'Uang Masuk', 0, 1)

    # Memastikan kolom klaster ada (antitesis error)
    if 'klaster_finansial' not in df.columns:
        def tentukan_klaster(row):
            kat = str(row['nama_kategori_label']).lower()
            if 'kebutuhan' in kat or 'income' in kat: return 'Klaster 0: Pengeluaran Prioritas'
            elif 'keinginan' in kat: return 'Klaster 1: Pengeluaran Impulsif'
            else: return 'Klaster 2: Pengeluaran Masa Depan'
        df['klaster_finansial'] = df.apply(tentukan_klaster, axis=1)

    df['tanggal'] = pd.to_datetime(df['tanggal'])
    df['tahun'] = df['tanggal'].dt.year
    df['bulan'] = df['tanggal'].dt.month
    return df

df_clean = load_financial_data()

# =========================================================================
# 3. SIDEBAR INTERAKTIF KONTROL PERIODE
# =========================================================================
st.sidebar.title("Fintrack AI")
st.sidebar.markdown("Kelola & Analisis Kesehatan Finansial Anda secara Real-Time.")
st.sidebar.markdown("---")

available_years = sorted(df_clean['tahun'].unique())
selected_years = st.sidebar.multiselect(
    "📅 Periode Tahun:",
    options=available_years,
    default=available_years
)

selected_months = st.sidebar.slider(
    "📆 Rentang Bulan Analisis:",
    min_value=1, max_value=12,
    value=(1, 12),
    format="%d"
)

df_active = df_clean[
    (df_clean['tahun'].isin(selected_years)) & 
    (df_clean['bulan'] >= selected_months[0]) & 
    (df_clean['bulan'] <= selected_months[1])
]

# Palet warna asisten keuangan premium
THEME_COLORS = ['#A1D6B4', '#E8A0A2', '#99B7F9', '#F4D793', '#C6A5EC']
COLOR_INCOME = '#10B981'   # Emerald Green
COLOR_EXPENSE = '#EF4444'  # Coral Red

# Warna khusus Klaster tugas tambahan
CLUSTER_COLORS = {
    'Klaster 0: Pengeluaran Prioritas': '#0284C7',  # Biru Stabilitas
    'Klaster 1: Pengeluaran Impulsif': '#EF4444',   # Merah Peringatan
    'Klaster 2: Pengeluaran Masa Depan': '#10B981'  # Hijau Pertumbuhan
}

# =========================================================================
# 4. HEADER UTAMA & KPI KARTU METRIK
# =========================================================================
st.title(" Fintrack AI")
st.markdown("Analisis komprehensif perilaku belanja, efisiensi kas, dan tren anomali musiman.")

if df_active.empty:
    st.warning("⚠️ Tidak ditemukan transaksi pada filter yang Anda pilih. Silakan sesuaikan kembali filter di panel samping.")
    st.stop()

income_pool = df_active[(df_active['tipe_label'] == 'Uang Masuk') | (df_active['tipe'] == 0)]['jumlah'].sum()
expense_pool = df_active[(df_active['tipe_label'] == 'Uang Keluar') | (df_active['tipe'] == 1)]['jumlah'].sum()
net_saving = income_pool - expense_pool
burn_rate_index = (expense_pool / income_pool * 100) if income_pool > 0 else 0

m_col1, m_col2, m_col3, m_col4 = st.columns(4)
with m_col1:
    st.metric(label="📥 Total Pemasukan", value=f"Rp {income_pool:,.0f}")
with m_col2:
    st.metric(label="📤 Total Pengeluaran", value=f"Rp {expense_pool:,.0f}")
with m_col3:
    st.metric(label="🌱 Surplus Bersih", value=f"Rp {net_saving:,.0f}", 
              delta=f"{(100 - burn_rate_index):.1f}% Tersisa", delta_color="normal")
with m_col4:
    status_burn = "⚠️ KRITIS" if burn_rate_index > 90 else "✅ AMAN"
    st.metric(label=f"📊 Burn Rate ({status_burn})", value=f"{burn_rate_index:.2f}%")

st.markdown("---")

# =========================================================================
# 5. LAYOUT STRUKTUR TAB JAWABAN + TUGAS TAMBAHAN KLASTER
# =========================================================================
tab_q1, tab_q2, tab_q3, tab_cluster = st.tabs([
    "🎯 Q1: Analisis Bocor Finansial",
    "⚖️ Q2: Efisiensi Arus Kas Makro",
    "📉 Q3: Pola Tren Akhir Tahun",
    "🤖 Tugas Tambahan: Segmentasi Klaster Finansial"
])

sns.set_theme(style="whitegrid")
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 120

# --- TAB 1 ---
with tab_q1:
    st.header("🎯 Analisis Struktur Pengeluaran Saat Kondisi 'Boros'")
    df_boros_active = df_active[(df_active['status_label'] == 'Boros') & ((df_active['tipe_label'] == 'Uang Keluar') | (df_active['tipe'] == 1))]
    
    if not df_boros_active.empty:
        c1, c2 = st.columns([1.2, 1])
        with c1:
            category_group = df_boros_active.groupby('nama_kategori_label')['jumlah'].sum().reset_index()
            fig_q1, ax_q1 = plt.subplots(figsize=(6, 5))
            fig_q1.patch.set_facecolor('#F8FAFC')
            ax_q1.set_facecolor('#F8FAFC')
            ax_q1.pie(category_group['jumlah'], labels=category_group['nama_kategori_label'], autopct='%1.2f%%', startangle=140, colors=THEME_COLORS, textprops={'fontsize': 11, 'weight': 'bold'}, wedgeprops={'edgecolor': '#F8FAFC', 'linewidth': 3})
            ax_q1.set_title("Proporsi Alokasi Dana Saat Rekor Finansial 'Boros'", fontsize=12, weight='bold', pad=15)
            st.pyplot(fig_q1)
            
        with c2:
            st.subheader("💡 AI Insight")
            
            # --- LOGIKA SAKTI UTK INSIGHT DINAMIS BERDASARKAN FILTER Bulanan/Tahunan ---
            total_dana_boros = category_group['jumlah'].sum()
            # Mencari baris data kategori yang nominal pengeluarannya paling besar saat itu
            top_category_row = category_group.loc[category_group['jumlah'].idxmax()]
            
            top_nama_kategori = top_category_row['nama_kategori_label']
            top_nominal = top_category_row['jumlah']
            # Hitung persentase real-time sesuai filter
            top_persentase = (top_nominal / total_dana_boros) * 100
            
            # Memunculkan teks pintar yang otomatis berubah isinya sesuai pergerakan filter
            st.markdown(f"""
            <div class="insight-box">
                Kategori <b>{top_nama_kategori}</b> mendominasi struktur pengeluaran sebesar 
                <b>{top_persentase:.2f}%</b> saat kondisi boros pada periode filter yang Anda pilih.
            </div>
            """, unsafe_allow_html=True)
            
            # Menampilkan tabel data pendukung
            category_group['Nominal'] = category_group['jumlah'].apply(lambda x: f"Rp {x:,.0f}")
            st.dataframe(category_group[['nama_kategori_label', 'Nominal']], use_container_width=True)
    else:
        st.success("🎉 Luar biasa! Tidak dideteksi status keuangan 'Boros' pada filter periode ini.")

# --- TAB 2 (BEBAS ERROR ANGKA 0) ---
with tab_q2:
    st.header("⚖️ Evaluasi Efisiensi Arus Kas Makro Agregat")
    c1, c2 = st.columns([1.5, 1])
    with c1:
        cashflow_summary = df_active.groupby('tipe_label')['jumlah'].sum().reset_index().sort_values(by='jumlah', ascending=False)
        fig_q2, ax_q2 = plt.subplots(figsize=(7, 3.5))
        fig_q2.patch.set_facecolor('#F8FAFC')
        ax_q2.set_facecolor('#F8FAFC')
        sns.barplot(y='tipe_label', x='jumlah', data=cashflow_summary, palette=[COLOR_INCOME, COLOR_EXPENSE], orient='h', ax=ax_q2, edgecolor='none')
        
        ax_q2.set_xticks([])
        ax_q2.set_xticklabels([])
        ax_q2.xaxis.grid(False)
        ax_q2.tick_params(axis='y', which='both', length=0, labelsize=11, labelcolor='#1E293B')
        ax_q2.yaxis.grid(False)
        
        max_v = cashflow_summary['jumlah'].max()
        ax_q2.set_xlim(0, max_v * 1.4)
        for p in ax_q2.patches:
            val = p.get_width()
            if val > 0:
                ax_q2.annotate(f'  Rp {val:,.0f}', (val, p.get_y() + p.get_height() / 2.), va='center', ha='left', fontsize=10, weight='bold', color='#1E293B')
        ax_q2.set_xlabel("Volume Likuiditas (Rupiah)", fontsize=9, weight='bold', color='#475569')
        ax_q2.set_ylabel("", fontsize=9)
        sns.despine(left=True, bottom=True)
        st.pyplot(fig_q2)
    with c2:
        st.subheader("💡 AI Insight")
        st.markdown(f'<div class="insight-box" style="background-color: #FFFBEB; border-left-color: #D97706; color: #92400E;">Burn Rate Anda mencapai <b>{burn_rate_index:.2f}%</b> dari total pendapatan bruto.</div>', unsafe_allow_html=True)

# --- TAB 3 ---
with tab_q3:
    st.header("季 Analisis Tren Siklus Konstan Akhir Tahun")
    df_expenses_only = df_active[(df_active['tipe_label'] == 'Uang Keluar') | (df_active['tipe'] == 1)].copy()
    if not df_expenses_only.empty:
        monthly_trend = df_expenses_only.groupby(['tahun', 'bulan'])['jumlah'].sum().reset_index()
        pivot_trend = monthly_trend.pivot(index='bulan', columns='tahun', values='jumlah')
        fig_q3, ax_q3 = plt.subplots(figsize=(11, 4.2))
        fig_q3.patch.set_facecolor('#F8FAFC')
        ax_q3.set_facecolor('#F8FAFC')
        for idx, current_year in enumerate(pivot_trend.columns):
            ax_q3.plot(pivot_trend.index, pivot_trend[current_year], marker='o', markersize=6, linewidth=2.5, label=f"Tahun {current_year}")
        ax_q3.set_xlabel("Bulan Distribusi", fontsize=10, weight='bold')
        ax_q3.set_ylabel("Total Pengeluaran (Rp)", fontsize=10, weight='bold')
        month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des']
        active_ticks = list(range(selected_months[0], selected_months[1] + 1))
        ax_q3.set_xticks(active_ticks)
        ax_q3.set_xticklabels([month_labels[i-1] for i in active_ticks])
        ax_q3.legend(loc='upper right')
        st.pyplot(fig_q3)

# --- 🔥 TAB NEW 4: SEGMENTASI KLASTER FINANSIAL (TUGAS TAMBAHAN) ---
with tab_cluster:
    st.header("🤖 Segmentasi Karakteristik Finansial Berbasis Klaster")
    st.markdown("Mengelompokkan transaksi keuangan ke dalam 3 klaster perilaku utama sesuai dengan arahan tugas tambahan.")
    
    # Kelompokkan total nominal pengeluaran per klaster
    df_out_only = df_active[(df_active['tipe_label'] == 'Uang Keluar') | (df_active['tipe'] == 1)]
    cluster_summary = df_out_only.groupby('klaster_finansial')['jumlah'].sum().reset_index()
    
    col_c1, col_c2 = st.columns([1.4, 1])
    
    with col_c1:
        # Membuat Donut Chart Premium untuk visualisasi Klaster (ANTI-TABRAKAN)
        fig_cl, ax_cl = plt.subplots(figsize=(6, 4.8))
        fig_cl.patch.set_facecolor('#F8FAFC')
        ax_cl.set_facecolor('#F8FAFC')
        
        # Mapping warna dinamis berdasarkan nama klaster
        colors_mapped = [CLUSTER_COLORS.get(name, '#CBD5E1') for name in cluster_summary['klaster_finansial']]
        
        # FIX UTAMA: Hapus labels=... agar teks panjang tidak merusak lingkaran, ganti pakai legend
        wedges, texts, autotexts = ax_cl.pie(
            cluster_summary['jumlah'],
            labels=None,                     # SAKTI: Menghilangkan teks label luar yang bikin berantakan
            autopct='%1.1f%%',
            startangle=140,                  
            pctdistance=0.75,                # Angka persentase pas di tengah warna kue
            colors=colors_mapped,
            wedgeprops=dict(width=0.4, edgecolor='#F8FAFC', linewidth=3) # Lebar donut chart
        )
        
        # Mengatur teks angka persentase di dalam warna kue agar kontras cerah
        for autotext in autotexts:
            autotext.set_color('white')      
            autotext.set_fontsize(10)
            autotext.set_weight('bold')
            
        # FIX KEDUA: Menampilkan kotak keterangan (Legend) rapi di bagian bawah chart
        ax_cl.legend(
            wedges, 
            cluster_summary['klaster_finansial'],
            title="Kategori Klaster",
            title_fontsize=9,
            loc="lower center",              # Ditaruh di bawah tengah agar simetris
            bbox_to_anchor=(0.5, -0.15),     # Mengatur posisi posisi kotak agar tidak menempel lingkaran
            fontsize=9,
            frameon=True,
            facecolor='#FFFFFF',
            edgecolor='#E2E8F0'
        )
            
        ax_cl.set_title("Distribusi Volume Alokasi Dana per Klaster Perilaku", fontsize=11, weight='bold', color='#0F172A', pad=10)
        st.pyplot(fig_cl)
        
    with col_c2:
        st.subheader("📋 Ringkasan Profil Segmentasi Klaster")
        st.markdown("""
        Berikut adalah karakteristik dari masing-masing segmen klaster finansial:
        - 🔵 **Klaster 0: Pengeluaran Prioritas** -> Kebutuhan primer wajib, operasional hidup dasar, dan tagihan tetap.
        - 🔴 **Klaster 1: Pengeluaran Impulsif** -> Keinginan, hobi, jajan konsumtif, dan pemborosan kas tak terencana.
        - 🟢 **Klaster 2: Pengeluaran Masa Depan** -> Alokasi tabungan, investasi jangka panjang, dan pos proteksi kekayaan.
        """)
        
        # Tampilkan tabel nominal rupiah per klaster
        cluster_summary['Total Nominal'] = cluster_summary['jumlah'].apply(lambda x: f"Rp {x:,.0f}")
        st.dataframe(
            cluster_summary[['klaster_finansial', 'Total Nominal']].rename(columns={'klaster_finansial': 'Segmen Klaster'}),
            use_container_width=True,
            hide_index=True
        )

# =========================================================================
# 6. FOOTER TABLE EXPLORER
# =========================================================================
st.markdown("---")
with st.expander("🔍 Pratinjau & Eksplorasi Data Transaksi Mentah Terfilter"):
    st.dataframe(df_active[['tanggal', 'tipe_label', 'nama_kategori_label', 'jumlah', 'status_label', 'klaster_finansial']], use_container_width=True)