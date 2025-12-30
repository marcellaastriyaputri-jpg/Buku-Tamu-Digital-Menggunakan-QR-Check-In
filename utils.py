import os
import pandas as pd
import streamlit as st
from datetime import datetime
from pyzbar.pyzbar import decode
from PIL import Image
import numpy as np
import qrcode

def init_files(tamu, log, qr_folder):
    os.makedirs("data", exist_ok=True)
    os.makedirs(qr_folder, exist_ok=True)

    if not os.path.exists(tamu):
        pd.DataFrame(columns=["id", "nama", "alamat"]).to_csv(tamu, index=False)

    if not os.path.exists(log):
        pd.DataFrame(columns=["id", "waktu"]).to_csv(log, index=False)

def load_csv(path):
    return pd.read_csv(path)

def save_csv(path, df):
    try:
        df.to_csv(path, index=False)
    except PermissionError:
        st.error("❌ Tutup file CSV yang sedang dibuka")

def generate_id(df):
    if df.empty:
        return "T001"
    last_id = str(df["id"].iloc[-1])
    number = int(last_id.replace("T", "")) + 1
    return f"T{number:03d}"

def add_tamu(path, nama, alamat):
    df = load_csv(path)
    new_id = generate_id(df)
    df.loc[len(df)] = [new_id, nama, alamat]
    save_csv(path, df)
    return new_id

def update_tamu(path, id_tamu, nama, alamat):
    df = load_csv(path)
    df.loc[df["id"] == id_tamu, ["nama", "alamat"]] = [nama, alamat]
    save_csv(path, df)

def delete_tamu(path, id_tamu):
    df = load_csv(path)
    df = df[df["id"] != id_tamu]
    save_csv(path, df)

def log_kunjungan(path_log, id_tamu):
    df = load_csv(path_log)
    df.loc[len(df)] = [id_tamu, datetime.now()]
    save_csv(path_log, df)

def generate_qr(text, folder):
    img = qrcode.make(text)
    path = f"{folder}/{text}.png"
    img.save(path)
    return path

def scan_qr_page(master, log):
    img_file = st.camera_input("Arahkan QR ke kamera")

    if img_file:
        img = Image.open(img_file)
        decoded = decode(np.array(img))

        if decoded:
            qr_id = decoded[0].data.decode("utf-8").strip()
            df_tamu = load_csv(master)

            if qr_id in df_tamu["id"].values:
                st.success("✅ Check-in berhasil")
                log_kunjungan(log, qr_id)
                st.dataframe(df_tamu[df_tamu["id"] == qr_id], use_container_width=True)
            else:
                st.error("❌ ID tidak ditemukan")
        else:
            st.error("❌ QR tidak terbaca")

def export_excel(df):
    df.to_excel("data/laporan_kunjungan.xlsx", index=False)
