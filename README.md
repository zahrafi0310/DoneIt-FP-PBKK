# DoneIt 

Platform gamifikasi kampus berbasis quest. Selesaikan tantangan, kumpulkan XP, dan naiki level.

---

## Tech Stack

- **Backend** — FastAPI + SQLAlchemy (SQLite)
- **Frontend** — Streamlit
- **Auth** — JWT + bcrypt

---

## Cara Menjalankan

### 1. Clone & Masuk Folder

```bash
git clone <url-repo>
cd DoneIt-FP-PBKK
```

### 2. Buat & Aktifkan Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

> Setiap kali buka terminal baru, ulangi langkah aktivasi venv di atas sebelum menjalankan project.

### 3. Install Dependencies

```bash
pip install fastapi uvicorn sqlalchemy python-jose bcrypt python-dotenv passlib streamlit requests python-multipart
```

### 4. Buat File `.env`

Buat file `.env` di dalam folder `backend/`

### 5. Inisialisasi Database & Buat Akun Admin

```bash
cd backend

python init_db.py        
python create_admin.py   
```
> default username dan password admin sudah terbentuk

### 6. Jalankan Backend & Frontend

Buka **2 terminal terpisah**, keduanya dengan venv aktif.

**Terminal 1 — Backend:**
```bash
cd backend
uvicorn main:app --reload
```

**Terminal 2 — Frontend:**
```bash
cd frontend
streamlit run app.py
```

---

## Akses Aplikasi

| Layanan | URL |
|---------|-----|
| Frontend (Streamlit) | http://localhost:8501 |
| Backend API | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |

---
## Catatan

- File `DoneIt.db` akan otomatis terbuat di folder `backend/` setelah `init_db.py` dijalankan.
- Folder `venv/` dan file `.env` sudah ada di `.gitignore` — tidak perlu di-commit.
- Langkah **3, 4, dan 5** hanya perlu dilakukan **sekali** saat pertama kali setup. Untuk run berikutnya, cukup aktifkan venv lalu langsung ke langkah 6.
