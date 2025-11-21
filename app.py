import streamlit as st
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
from PIL import Image
import io
import time 

# --- FUNGSI CSS KUSTOM UNTUK TAMPILAN (VISUAL UPGRADE MAKSIMAL) ---
def inject_custom_css():
    st.markdown("""
        <style>
        /* Variabel Warna */
        :root {
            --primary-color: #4CAF50; /* Hijau Ceria */
            --secondary-color: #00796b; /* Teal Gelap */
            --background-color: #f0f8ff; /* Biru Langit Sangat Muda */
            --card-color: #ffffff; /* Putih Bersih */
        }
        
        /* Gaya Global */
        .stApp {
            background-color: var(--background-color); 
            color: #333333;
        }
        
        /* Header dan Subheader */
        h1 {
            color: var(--secondary-color);
            font-size: 2.5em;
            text-shadow: 1px 1px 3px rgba(0, 121, 107, 0.2);
        }
        h2, h3, h4 {
            color: #1a1a1a;
            border-bottom: 2px solid #e0f7fa; /* Garis bawah elegan */
            padding-bottom: 5px;
            margin-top: 20px;
        }
        .stCaption {
            color: #666666;
            font-style: italic;
        }
        
        /* Box Info/Warning (Lebih Ceria) */
        .stAlert {
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            border-left: 6px solid;
        }

        /* --- STYLING CHAT BUBBLE (Tampilan Unik & Modern) --- */
        
        /* Kontainer Chat Message */
        div.stChatMessage {
            margin: 10px 0;
        }

        /* Chat Bubble Asisten (SiPintar) */
        div[data-testid="stChatMessage"]:nth-child(even) [data-testid="stChatMessageContent"] {
            background-color: var(--card-color) !important; 
            border-radius: 15px 15px 15px 5px; /* Bubble unik */
            box-shadow: 0 3px 8px rgba(0, 121, 107, 0.15); /* Shadow halus */
            border-left: 4px solid var(--primary-color); /* Garis aksen */
            padding: 15px;
        }
        
        /* Chat Bubble User */
        div[data-testid="stChatMessage"]:nth-child(odd) [data-testid="stChatMessageContent"] {
            background-color: #e0f8f0 !important; /* Latar belakang hijau muda */
            border-radius: 15px 15px 5px 15px;
            border-right: 4px solid var(--secondary-color);
            padding: 15px;
            box-shadow: 0 3px 8px rgba(0, 0, 0, 0.1);
        }

        /* --- STYLING INPUT DAN TOMBOL --- */

        /* Input Teks */
        [data-testid="stTextInput"] > div > div > input {
            border-radius: 10px;
            border: 2px solid #ced4da;
            transition: border-color 0.3s, box-shadow 0.3s;
            padding: 10px 15px;
        }
        [data-testid="stTextInput"] > div > div > input:focus {
            border-color: var(--primary-color);
            box-shadow: 0 0 0 0.2rem rgba(76, 175, 80, 0.25);
        }

        /* Tombol Kirim / Primary Button */
        div.stButton button, button[data-testid="baseButton-primary"] {
            background-color: var(--primary-color) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 10px 20px !important;
            font-weight: bold;
            transition: background-color 0.2s, transform 0.1s;
        }
        
        div.stButton button:hover, button[data-testid="baseButton-primary"]:hover {
            background-color: #43a047 !important; /* Hijau lebih gelap saat hover */
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        }
        
        /* Tombol Sekunder */
        button[data-testid="baseButton-secondary"] {
            background-color: var(--card-color) !important;
            color: var(--secondary-color) !important;
            border: 2px solid var(--secondary-color) !important;
            border-radius: 10px !important;
        }
        
        /* File Uploader (Memberi Shadow) */
        [data-testid="stFileUploader"] {
             border-radius: 12px;
             padding: 15px;
             background-color: var(--card-color);
             box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
        }

        /* Mengatur posisi tombol Kirim di Form Chat/Ringkas/Terjemah */
        #chat_form button[type="submit"], #ringkas_form button[type="submit"], #terjemah_form button[type="submit"] {
            margin-top: 15px !important; /* Posisikan tombol agar pas */
            width: 100%; /* Lebar penuh di kolomnya */
        }
        
        </style>
        """, unsafe_allow_html=True)

# Panggil fungsi CSS di awal script
st.set_page_config(page_title="SiPintar - Asisten Belajar AI", page_icon="🤖", layout="wide")

# Panggil fungsi CSS di awal script
inject_custom_css()


# Load API key dari .env (asumsi file dan key sudah disiapkan)
load_dotenv()
# Menggunakan placeholder key 
genai.configure(api_key="AIzaSyDs_zoT19Cc9uA9JXc9EyXKBHSsclX19KY") 

# --- FUNGSI BANTUAN UNTUK MULTIMODAL ---
def get_gemini_content(prompt, uploaded_file=None, model=None):
    content = []
    
    if uploaded_file is not None:
        try:
            if uploaded_file.type.startswith('image/'):
                image = Image.open(uploaded_file)
                content.append(image)
            else:
                content.append(f"[File {uploaded_file.type} diunggah: {uploaded_file.name}. Instruksi diproses bersama file.]")
                
        except Exception as e:
            # Gunakan st.error untuk menangani error file
            st.error(f"Gagal memproses file yang diunggah: {e}")
    
    content.append(prompt)
    
    try:
        # Tambahkan animasi dan jeda loading yang unik
        with st.spinner("🚀 SiPintar sedang merumuskan jawaban terbaik untukmu..."):
             time.sleep(1) # Jeda minimal 1 detik untuk efek loading
             response = model.generate_content(content)
             return response.text
    except Exception as e:
        return f"Terjadi error saat menghubungi Gemini API: {e}"

# Setting model Gemini 2.5 Flash
model_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
}

safety_settings = [
    {"category": HarmCategory.HARM_CATEGORY_HARASSMENT, "threshold": HarmBlockThreshold.BLOCK_NONE},
    {"category": HarmCategory.HARM_CATEGORY_HATE_SPEECH, "threshold": HarmBlockThreshold.BLOCK_NONE},
    {"category": HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, "threshold": HarmBlockThreshold.BLOCK_NONE},
    {"category": HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, "threshold": HarmBlockThreshold.BLOCK_NONE},
]

gemini_model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    generation_config=model_config,
    safety_settings=safety_settings,
    system_instruction="Kamu adalah SiPintar, asisten belajar yang ramah untuk siswa SMA/SMK di Indonesia. Jawab SEMUA dalam bahasa Indonesia yang mudah dipahami, jelaskan langkah demi langkah, gunakan contoh jika perlu, dan selalu semangati siswa. Terima input gambar, audio, atau teks."
)


# Header yang Lebih Menarik dan Unik
st.title("🚀 SiPintar - Asisten Belajar Premium")
st.caption("AI Cerdas, Ramah, dan Selalu Siap Membantumu Meraih Prestasi Terbaik!")

# Tabs Baru (Menggunakan emoji yang lebih menarik)
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💬 Chat Belajar", 
    "📚 Ringkas Materi", 
    "✍ Buat Soal", 
    "🌐 Terjemah Inggris", 
    "🏫 Sistem Kelas"
])

# ===============================================
## 💬 Chatbot Belajar 
# ===============================================
with tab1:
    st.subheader("💬 Chat Belajar Interaktif (Teks, Foto, & Video)")
    
    # Inisialisasi state
    if "messages_chat" not in st.session_state:
        st.session_state.messages_chat = [{
            "role": "assistant",
            "content": "Halo! Saya SiPintar, asisten belajarmu. Ada yang bisa saya bantu hari ini? Jangan sungkan bertanya, ya! Semangat!"
        }]
    
    # --- Tampilkan riwayat chat ---
    for message in st.session_state.messages_chat:
        with st.chat_message(message["role"]):
            if message.get("image"):
                st.image(message["image"], caption="File yang Diunggah", width=200)
            st.markdown(message["content"])

    # --- INPUT AREA (Vertikal seperti di gambar) ---
    st.markdown("---")
    
    with st.form(key='chat_form', clear_on_submit=True):
        
        st.caption("Unggah file foto/video dan masukkan pertanyaan Anda di kolom di bawah.")
        
        # 1. File Uploader (Besar, Default Streamlit)
        uploaded_file_chat = st.file_uploader(
            "Upload File", 
            type=['jpg', 'jpeg', 'png', 'mp4', 'mov'], 
            key="chat_uploader_tab1",
            label_visibility="collapsed" 
        )
            
        # 2. Area Input dan Tombol Kirim (Horizontal)
        col_input, col_submit = st.columns([9, 1])
        
        with col_input:
            prompt = st.text_input("Ketik pertanyaan atau instruksi Anda...", 
                                    key="chat_input_text_area", 
                                    label_visibility="collapsed",
                                    placeholder="Tanya apa saja tentang pelajaranmu...")

        with col_submit:
             # Tombol submit (Menggunakan label kosong agar CSS bisa mengatur tingginya)
             submit_button = st.form_submit_button(label='Kirim')
             
    if uploaded_file_chat and not submit_button:
        st.info(f"File *{uploaded_file_chat.name}* diunggah! Tekan *Kirim* untuk memproses.")


    if submit_button and prompt:
        
        # Tambahkan pesan user
        image_to_display = None
        current_uploaded_file = st.session_state.chat_uploader_tab1 # Ambil file dari session state
        
        if current_uploaded_file and current_uploaded_file.type.startswith('image/'):
            image_to_display = Image.open(current_uploaded_file)
        
        st.session_state.messages_chat.append({
            "role": "user", 
            "content": prompt, 
            "image": image_to_display
        })
        
        with st.chat_message("user"):
            if image_to_display:
                st.image(image_to_display, caption="File yang Diunggah", width=200)
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # Panggilan dengan spinner unik
            response_text = get_gemini_content(
                prompt, 
                current_uploaded_file, 
                model=gemini_model
            )
            st.markdown(response_text)

        # Simpan respons assistant
        st.session_state.messages_chat.append({"role": "assistant", "content": response_text})
        st.rerun() 

# ===============================================
## 📚 Ringkas Materi 
# ===============================================
with tab2:
    st.subheader("📚 Ringkas Materi Cepat")
    
    # OUTPUT
    if "ringkasan_output" not in st.session_state:
        st.session_state.ringkasan_output = ""
    
    if st.session_state.ringkasan_output:
        st.success("✨ Ini dia ringkasan materi terbaik untukmu!")
        st.markdown(st.session_state.ringkasan_output)
    
    st.markdown("---")

    # INPUT AREA (Vertical)
    st.caption("Unggah file foto materi atau masukkan teks materi di kolom di bawah.")
    
    with st.form(key='ringkas_form', clear_on_submit=False):
        
        # 1. File Uploader (Besar)
        uploaded_file_ringkas = st.file_uploader(
            "Upload File Materi", 
            type=['jpg', 'jpeg', 'png'], 
            key="ringkas_uploader",
            label_visibility="collapsed"
        )

        # 2. Area Input dan Tombol Kirim (Horizontal)
        col_input, col_submit = st.columns([9, 1])
        
        with col_input:
             materi = st.text_input("Ketik materi di sini...", 
                                    key="materi_input", 
                                    label_visibility="collapsed",
                                    placeholder="Ketik materi yang ingin diringkas di sini (Misal: Siklus Krebs)...")

        with col_submit:
             ringkas_submit = st.form_submit_button(label='Ringkas', type="primary")

    if ringkas_submit:
        if materi.strip() or uploaded_file_ringkas:
            
            final_prompt = f"""Ringkas materi berikut menjadi poin-poin penting yang mudah dihafal siswa SMA. 
            Gunakan bullet point, nomor, dan bahasa Indonesia sederhana. Materi/Instruksi Tambahan: {materi}"""
            
            response_text = get_gemini_content(
                final_prompt, 
                uploaded_file_ringkas, 
                model=gemini_model
            )
            
            st.session_state.ringkasan_output = response_text
            st.rerun() 
        else:
            st.warning("Silakan masukkan materi atau unggah gambar dulu ya!")

# ===============================================
## ✍ Buat Soal 
# ===============================================
with tab3:
    st.subheader("✍ Generator Soal Otomatis + Kunci Jawaban")
    col1, col2 = st.columns(2)
    with col1:
        topik = st.text_input("Topik/Materi", placeholder="Misal: Persamaan Kuadrat")
        kelas = st.selectbox("Kelas", ["Kelas 10", "Kelas 11", "Kelas 12"])
    with col2:
        jumlah_soal = st.number_input("Jumlah Soal", min_value=3, max_value=20, value=10)
        jenis_soal = st.selectbox("Jenis Soal", ["Pilihan Ganda", "Essay/Uraian", "Campur"])

    if st.button("Buat Soal Sekarang", type="primary"):
        if topik.strip():
            with st.spinner("Membuat soal..."):
                time.sleep(1) 
                prompt = f"""Buatlah {jumlah_soal} soal {jenis_soal.lower()} tentang "{topik}" untuk siswa {kelas}.
                Berikan tingkat kesulitan sedang.
                Sertakan kunci jawaban/pembahasan lengkap di bagian bawah (pisahkan dengan garis ---).
                Format rapi dengan nomor dan markdown."""
                response = gemini_model.generate_content(prompt)
                
                st.success(f"✅ Soal siap! {topik} - {kelas}")
                st.markdown(response.text)
        else:
            st.warning("Masukkan topik dulu ya!")

# ===============================================
## 🌐 Terjemah Inggris
# ===============================================
with tab4:
    st.subheader("🌐 Terjemah + Penjelasan Bahasa Inggris")
    
    # OUTPUT
    if "terjemah_output" not in st.session_state:
        st.session_state.terjemah_output = ""
    
    if st.session_state.terjemah_output:
        st.success("📝 Hasil Terjemahan & Penjelasan:")
        st.markdown(st.session_state.terjemah_output)
    
    st.markdown("---")

    # INPUT AREA (Vertical)
    st.caption("Unggah file foto teks atau masukkan teks bahasa Inggris di kolom di bawah.")
    
    with st.form(key='terjemah_form', clear_on_submit=False):
        
        # 1. File Uploader (Besar)
        uploaded_file_terjemah = st.file_uploader(
            "Upload File Teks", 
            type=['jpg', 'jpeg', 'png'], 
            key="terjemah_uploader",
            label_visibility="collapsed"
        )
        
        # 2. Area Input dan Tombol Kirim (Horizontal)
        col_input, col_submit = st.columns([9, 1])

        with col_input:
            teks_inggris = st.text_input("Masukkan teks bahasa Inggris:", 
                                        key="teks_inggris_input", 
                                        label_visibility="collapsed",
                                        placeholder="Ketik teks bahasa Inggris di sini...")
        
        with col_submit:
            terjemah_submit = st.form_submit_button(label='Terjemah', type="primary")

    if terjemah_submit:
        if teks_inggris.strip() or uploaded_file_terjemah:
            
            final_prompt = f"""Lakukan 3 hal ini untuk teks yang diberikan (atau teks dalam gambar):
            1. Terjemahkan ke bahasa Indonesia yang natural
            2. Jelaskan grammar/kosa kata penting yang ada di teks
            3. Berikan contoh kalimat serupa
            
            Teks yang dimasukkan: {teks_inggris}"""
            
            response_text = get_gemini_content(
                final_prompt, 
                uploaded_file_terjemah, 
                model=gemini_model
            )
            
            st.session_state.terjemah_output = response_text
            st.rerun() 
        else:
            st.warning("Masukkan teks atau unggah gambar dulu ya!")

# ===============================================
## 🏫 Sistem Kelas 
# ===============================================
with tab5:
    st.header("🏫 Sistem Operasi Kelas")
    st.error("⚠ PENTING: Fitur ini hanya simulasi. Untuk penyimpanan data permanen, dibutuhkan Server Backend dan Database sesungguhnya.")
    
    st.subheader("🔗 Koneksi Backend (Simulasi)")
    backend_uri = st.text_input(
        "Endpoint Server / Database URI", 
        placeholder="http://api.sipintar-kelas.com/attendance",
        key="backend_uri"
    )
    
    if st.button("Simulasikan Koneksi", key="connect_backend"):
        if backend_uri.strip():
            st.success("Koneksi disimulasikan! Anda siap mengelola data.")
        else:
            st.warning("Silakan masukkan URI/Endpoint untuk simulasi koneksi.")
            
    st.markdown("---")

    # Inisialisasi state untuk fitur sistem kelas
    if "is_manager_logged_in" not in st.session_state:
        st.session_state.is_manager_logged_in = False
    if "student_list" not in st.session_state:
        st.session_state.student_list = []
    if "attendance_data" not in st.session_state:
        st.session_state.attendance_data = {}

    # --- Simulasi Login Ketua/Wali Kelas ---
    if not st.session_state.is_manager_logged_in:
        with st.expander("🔑 Login Manager Kelas (Simulasi)"):
            st.caption("Gunakan username: admin dan password: sipintar")
            col_login_1, col_login_2, col_login_3 = st.columns([1, 1, 1])
            with col_login_1:
                username = st.text_input("Username", value="", key="class_user_v2")
            with col_login_2:
                password = st.text_input("Password", type="password", value="", key="class_pass_v2")
            with col_login_3:
                st.markdown("<br>", unsafe_allow_html=True) 
                if st.button("Masuk", key="login_btn_v2", type="primary"):
                    if username == "admin" and password == "sipintar":
                        st.session_state.is_manager_logged_in = True
                        st.success("Login Berhasil! Selamat datang, Manager Kelas.")
                        st.rerun() 
                    else:
                        st.error("Username atau Password salah.")

    if st.session_state.is_manager_logged_in:
        
        st.subheader("🛠 Konfigurasi Daftar Murid")
        default_data = st.session_state.student_list if st.session_state.student_list else [{"Absen": 1, "Nama": "Nama Murid A"}, {"Absen": 2, "Nama": "Nama Murid B"}]
        
        edited_df = st.data_editor(
            default_data,
            column_config={
                "Absen": st.column_config.NumberColumn("No. Absen", min_value=1, format="%d"),
                "Nama": st.column_config.TextColumn("Nama Murid", required=True)
            },
            num_rows="dynamic",
            use_container_width=True
        )

        if st.button("Simpan Daftar Murid", key="save_students_v2", type="secondary"):
            st.session_state.student_list = edited_df.to_dict('records')
            
            for student in st.session_state.student_list:
                name = student['Nama']
                if name not in st.session_state.attendance_data:
                    # Inisialisasi data kehadiran untuk murid baru
                    st.session_state.attendance_data[name] = {
                        "created_at": datetime.now().isoformat(),
                        "attendance": []
                    }
            st.success("Daftar murid berhasil disimpan.")
            st.rerun()