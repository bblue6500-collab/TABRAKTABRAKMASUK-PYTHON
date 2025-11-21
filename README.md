# SiPintar - Asisten Belajar Pintar Berbasis AI

## Latar Belakang
Dalam proses pembelajaran, banyak siswa mengalami kesulitan ketika harus mencari penjelasan cepat, memahami materi yang panjang, atau menerjemahkan teks berbahasa Inggris. Aplikasi yang tersedia saat ini sering kali hanya menawarkan satu fungsi, sehingga siswa perlu berganti-ganti platform untuk memenuhi kebutuhan belajar mereka. Kondisi ini kurang efisien dan dapat menghambat pemahaman materi. Berdasarkan permasalahan tersebut, SiPintar dikembangkan sebagai asisten bot pintar berbasis Python yang mampu menyediakan berbagai kebutuhan belajar dalam satu aplikasi, sehingga proses belajar menjadi lebih mudah, cepat, dan efektif.

## Permasalahan yang Dijawab
- Sulit memahami materi pelajaran sendirian
- Tidak ada teman/tutor 24 jam
- Guru butuh waktu lama membuat bahan ajar
- Bahasa Inggris sering jadi kendala

## Fitur
- Chatbot belajar semua mata pelajaran (dengan riwayat)
- Ringkas materi otomatis jadi poin-poin
- Generator soal + kunci jawaban (pilihan ganda/essay)
- Terjemah + jelaskan grammar bahasa Inggris

## Teknologi
- Python + Streamlit
- Google Gemini 1.5 Flash API (gratis 15 juta token gratis/bulan)

## Link Demo Online
https://sipintar-belajar.streamlit.app  ← (ganti dengan link kamu setelah deploy)

Dibuat untuk memenuhi tugas Proyek TIK Pemerintah Provinsi Jawa Timur 2025

## Setup & Running Locally (API key required)

1. Create a Python virtual environment and install dependencies:

```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

2. Provide your Gemini/Generative API key. The app looks for `GEMINI_API_KEY` or `GENAI_API_KEY`.

- Recommended (create a `.env` file in the project root):

```
GEMINI_API_KEY=your_real_gemini_api_key_here
```

- Or set it temporarily in Windows `cmd` before running:

```cmd
set GEMINI_API_KEY=your_real_gemini_api_key_here
streamlit run app.py
```

3. Run the Streamlit app:

```cmd
streamlit run app.py
```

Troubleshooting
- If you see the message: `Model not configured. Please set the environment variable GEMINI_API_KEY (or GENAI_API_KEY) in a .env file or your environment and restart the app.` — that means the app did not detect an API key. Add the key to `.env` or set the environment variable and restart Streamlit.
- If you get an API error like `API key not valid`, check that the key is active, has the correct permissions, and billing/quota is enabled.
- For local debugging, check your virtual environment and ensure `python` used to run Streamlit is the same interpreter that has the packages installed.

Security note

- Do not commit your `.env` file or API key to source control. Use environment variables for deployments and secrets managers for production.
