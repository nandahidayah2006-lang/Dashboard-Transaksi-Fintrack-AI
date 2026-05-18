# =========================================================
# DASHBOARD.PY
# Dashboard Analisis Keuangan Personal
# =========================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =========================================================
# CONFIG PAGE
# =========================================================

st.set_page_config(
    page_title="Dashboard Analisis Keuangan",
    layout="wide"
)

# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():
    df = pd.read_excel("DATASET_KEUANGAN_UPDATED.xlsx")

    df["tanggal"] = pd.to_datetime(df["tanggal"])
    df["tahun"] = df["tanggal"].dt.year
    df["bulan_nama"] = df["tanggal"].dt.strftime("%b")

    return df

df = load_data()

# =========================================================
# STYLE
# =========================================================

sns.set_theme(style="whitegrid")

WARNA_PASTEL = [
    '#E8A0A2',
    '#A1D6B4',
    '#99B7F9',
    '#F4D793',
    '#C6A5EC'
]

# =========================================================
# HEADER
# =========================================================

st.title("📊 Dashboard Analisis Keuangan Personal")

st.markdown("""
Dashboard ini menampilkan hasil analisis:
- Kontribusi kategori pengeluaran terhadap status boros
- Perbandingan income dan expenses
- Tren pengeluaran bulanan
""")

# =========================================================
# METRIC CARDS
# =========================================================

income_total = df[df["tipe_label"] == "Masuk"]["jumlah"].sum()
expense_total = df[df["tipe_label"] == "Keluar"]["jumlah"].sum()
saldo_akhir = df["saldo akhir"].iloc[-1]

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Income",
    f"Rp {income_total:,.0f}"
)

col2.metric(
    "Total Expenses",
    f"Rp {expense_total:,.0f}"
)

col3.metric(
    "Saldo Akhir",
    f"Rp {saldo_akhir:,.0f}"
)

# =========================================================
# FILTER TAHUN
# =========================================================

tahun_pilih = st.selectbox(
    "Pilih Tahun",
    sorted(df["tahun"].unique())
)

df_filter = df[df["tahun"] == tahun_pilih]

# =========================================================
# GRAFIK 1
# PIE CHART STATUS BOROS
# =========================================================

st.subheader(
    "Kontribusi Kategori Pengeluaran Saat Status 'Boros'"
)

df_boros = df_filter[
    (df_filter["status_label"] == "Boros") &
    (df_filter["tipe_label"] == "Keluar")
]

kategori_boros = (
    df_boros
    .groupby("nama_kategori_label")["jumlah"]
    .sum()
)

fig1, ax1 = plt.subplots(figsize=(8,6))

ax1.pie(
    kategori_boros,
    labels=kategori_boros.index,
    autopct='%1.2f%%',
    startangle=90,
    colors=WARNA_PASTEL,
    wedgeprops={'edgecolor':'white', 'linewidth':3},
    textprops={'fontsize':12, 'fontweight':'bold'}
)

ax1.set_title(
    "Kontribusi Kategori Pengeluaran Saat Boros",
    fontsize=16,
    fontweight='bold'
)

st.pyplot(fig1)

# =========================================================
# GRAFIK 2
# BAR CHART INCOME VS EXPENSES
# =========================================================

st.subheader(
    "Perbandingan Arus Kas: Income vs Expenses"
)

income = df_filter[
    df_filter["tipe_label"] == "Masuk"
]["jumlah"].sum()

expenses = df_filter[
    df_filter["tipe_label"] == "Keluar"
]["jumlah"].sum()

fig2, ax2 = plt.subplots(figsize=(10,5))

kategori = ["Masuk", "Keluar"]
nilai = [income, expenses]

bars = ax2.barh(
    kategori,
    nilai,
    color=[WARNA_PASTEL[1], WARNA_PASTEL[0]]
)

ax2.set_title(
    "Perbandingan Arus Kas Agregat",
    fontsize=16,
    fontweight='bold'
)

ax2.set_xlabel(
    "Total Nominal (Rupiah)",
    fontsize=12,
    fontweight='bold'
)

for bar in bars:

    width = bar.get_width()

    ax2.text(
        width + 10000000,
        bar.get_y() + bar.get_height()/2,
        f"Rp {width:,.0f}",
        va='center',
        fontsize=12,
        fontweight='bold'
    )

st.pyplot(fig2)

# =========================================================
# GRAFIK 3
# LINE CHART TREN BULANAN
# =========================================================

st.subheader(
    "Analisis Tren Pengeluaran Bulanan"
)

pengeluaran = df[
    df["tipe_label"] == "Keluar"
]

monthly = (
    pengeluaran
    .groupby(
        ["tahun", "bulan_nama"]
    )["jumlah"]
    .sum()
    .reset_index()
)

urutan_bulan = [
    "Jan","Feb","Mar","Apr","May","Jun",
    "Jul","Aug","Sep","Oct","Nov","Dec"
]

monthly["bulan_nama"] = pd.Categorical(
    monthly["bulan_nama"],
    categories=urutan_bulan,
    ordered=True
)

monthly = monthly.sort_values(
    ["tahun", "bulan_nama"]
)

fig3, ax3 = plt.subplots(figsize=(14,6))

for i, tahun in enumerate(monthly["tahun"].unique()):

    data_tahun = monthly[
        monthly["tahun"] == tahun
    ]

    ax3.plot(
        data_tahun["bulan_nama"],
        data_tahun["jumlah"],
        marker='o',
        linewidth=3,
        markersize=8,
        label=f"Tahun {tahun}",
        color=WARNA_PASTEL[i % len(WARNA_PASTEL)]
    )

ax3.set_title(
    "Analisis Tren Pengeluaran Bulanan",
    fontsize=18,
    fontweight='bold'
)

ax3.set_xlabel(
    "Bulan",
    fontsize=12,
    fontweight='bold'
)

ax3.set_ylabel(
    "Total Pengeluaran",
    fontsize=12,
    fontweight='bold'
)

ax3.legend()

st.pyplot(fig3)

# =========================================================
# DATASET
# =========================================================

st.subheader("Preview Dataset")

st.dataframe(df_filter)

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.markdown("""
📌 Dashboard dibuat menggunakan:
- Python
- Streamlit
- Pandas
- Matplotlib
- Seaborn
""")