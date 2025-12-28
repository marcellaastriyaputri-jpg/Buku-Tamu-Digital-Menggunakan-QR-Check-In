import streamlit as st
import pandas as pd
from utils import *

# ================= LOAD CSS =================
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.set_page_config(
    page_title="Buku Tamu Digital QR",
    layout="centered"
)

DATA_TAMU = "data/tamu.csv"
DATA_LOG = "data/kunjungan.csv"
QR_FOLDER = "qr"

init_files(DATA_TAMU, DATA_LOG, QR_FOLDER)

# ================= LOGIN =================
if "role" not in st.session_state:
    st.session_state.role = None

st.sidebar.title("🔐 Login")
role = st.sidebar.selectbox("Masuk sebagai", ["Tamu", "Admin"])
if st.sidebar.button("Login"):
    st.session_state.role = role

if st.session_state.role is None:
    st.stop()

# =================================================
# 👤 MODE TAMU
# =================================================
if st.session_state.role == "Tamu":

    menu = st.sidebar.radio("Menu", ["Isi Buku Tamu", "Scan QR"])

    if menu == "Isi Buku Tamu":
        st.title("📝 Isi Buku Tamu")

        with st.form("form_tamu"):
            nama = st.text_input("Nama")
            alamat = st.text_input("Alamat")
            submit = st.form_submit_button("Simpan")

        if submit:
            if nama.strip() == "" or alamat.strip() == "":
                st.error("Nama dan alamat wajib diisi")
            else:
                new_id = add_tamu(DATA_TAMU, nama, alamat)
                log_kunjungan(DATA_LOG, new_id)
                qr_path = generate_qr(new_id, QR_FOLDER)

                st.success("Data berhasil disimpan")
                st.write(f"**ID Anda:** {new_id}")
                st.image(qr_path, caption="QR Code Anda")

                with open(qr_path, "rb") as f:
                    st.download_button(
                        "Download QR Code",
                        f,
                        file_name=f"{new_id}.png"
                    )

    else:
        st.title("📷 Scan QR")
        scan_qr_page(DATA_TAMU, DATA_LOG)

# =================================================
# 🔐 MODE ADMIN
# =================================================
else:

    menu = st.sidebar.radio(
        "Menu",
        ["Dashboard", "Data Tamu", "Laporan", "Tentang"]
    )

    if menu == "Dashboard":
        st.title("📊 Dashboard")

        df_tamu = load_csv(DATA_TAMU)
        df_log = load_csv(DATA_LOG)
        df_log["waktu"] = pd.to_datetime(df_log["waktu"])

        today = pd.Timestamp.now().date()

        col1, col2, col3 = st.columns(3)
        col1.metric("👥 Total Tamu", len(df_tamu))
        col2.metric("📊 Total Kunjungan", len(df_log))
        col3.metric("📅 Hari Ini", len(df_log[df_log["waktu"].dt.date == today]))

        st.subheader("📈 Grafik Kunjungan Hari Ini")

        df_today = df_log[df_log["waktu"].dt.date == today]
        if df_today.empty:
            st.info("Belum ada kunjungan hari ini")
        else:
            grafik = df_today.groupby(df_today["waktu"].dt.hour).size()
            st.line_chart(grafik)

    elif menu == "Data Tamu":
        st.title("📋 Data Tamu")

        df = load_csv(DATA_TAMU)
        st.dataframe(df, use_container_width=True)

        st.subheader("✏ Update Data")
        with st.form("update"):
            id_u = st.text_input("ID Tamu (T001)")
            nama_u = st.text_input("Nama Baru")
            alamat_u = st.text_input("Alamat Baru")
            if st.form_submit_button("Update"):
                update_tamu(DATA_TAMU, id_u, nama_u, alamat_u)
                st.success("Data berhasil diperbarui")

        st.subheader("🗑 Hapus Data")
        id_d = st.text_input("ID yang akan dihapus")
        if st.button("Hapus"):
            delete_tamu(DATA_TAMU, id_d)
            st.warning("Data berhasil dihapus")

    elif menu == "Laporan":
        st.title("📊 Laporan Kunjungan")

        df_log = load_csv(DATA_LOG)
        df_log["waktu"] = pd.to_datetime(df_log["waktu"])

        col1, col2 = st.columns(2)
        start = col1.date_input("Tanggal Mulai")
        end = col2.date_input("Tanggal Akhir")

        df_filter = df_log
        if st.button("Filter"):
            df_filter = df_log[
                (df_log["waktu"].dt.date >= start) &
                (df_log["waktu"].dt.date <= end)
            ]

        st.dataframe(df_filter, use_container_width=True)

        if st.button("Export Excel"):
            export_excel(df_filter)
            st.success("Laporan berhasil diexport")

    else:
        st.title("Tentang Aplikasi")
        st.markdown("""
        **Buku Tamu Digital Berbasis QR Code**

        - Python & Streamlit
        - QR Code otomatis
        - Dashboard Admin
        - Export laporan

        **Tujuan:**  
        Mempermudah pencatatan dan monitoring kunjungan.
        """)
