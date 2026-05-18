# 📊 Personal Financial Analysis Dashboard

## 📌 Project Description
This project is a personal financial analysis system built using Python and Streamlit. The system analyzes user financial transaction data to identify spending behavior patterns and classify financial status into three categories:

- Hemat (Saving)
- Normal
- Boros (High Spending)

The dashboard also provides interactive visualizations to help users understand their income, expenses, and monthly spending trends.

---

# 🎯 Project Objectives

The objectives of this project are:

- Analyze the contribution of spending categories toward financial status.
- Compare total income and total expenses.
- Analyze monthly spending trends over time.
- Prepare a realistic financial dataset for machine learning and forecasting purposes.
- Build an interactive dashboard visualization using Streamlit.

---

# 🗂 Dataset Attributes

The dataset contains the following attributes:

| Attribute | Description |
|---|---|
| tanggal | Transaction date |
| bulan | Month of transaction |
| nama_kategori | Transaction category code |
| nama_kategori_label | Category name |
| deskripsi | Transaction description |
| tipe | Transaction type code |
| tipe_label | Income / Expense |
| saldo awal | Balance before transaction |
| jumlah | Transaction amount |
| saldo akhir | Balance after transaction |
| status | Financial status code |
| status_label | Financial status label |
| prediksi_pengeluaran | Predicted expense value |

---

# 🧠 Financial Status Logic

Financial status is determined using the comparison between:

```python
saldo_akhir / total_income_bulanan
