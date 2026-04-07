# Foggy Weather Detection System

This project is a high-performance, end-to-end deep learning web application built to enhance visibility and detect objects in extreme foggy conditions. The architecture uses a real mathematical Dehazing algorithm (CLAHE via OpenCV) integrated with a modern Neural Network (Ultralytics YOLOv8) wrapped gracefully by a FastAPI/React stack.

The project is structured vertically across two main layers:
- **`backend/`**: A fully decoupled FastAPI service interacting with an SQLite database via SQLAlchemy. It streams large video binaries asynchronously into a background AI Processing Pipeline running YOLO and OpenCV.
- **`frontend/`**: A sleek glass-morphism React UI bundled by Vite, securely orchestrating the video upload payload, dynamically polling the backend, and drawing interactive graphical results.

---

## ⚡ Installation & Setup

### 1. Project Root Configuration (Backend/AI)
Open your terminal in the Root directory of this repository before proceeding.

```shell
# 1. Spin up your Python Virtual Environment
python -m venv venv

# Activation for Windows:
.\venv\Scripts\Activate.ps1
# Activation for Mac/Linux:
source venv/bin/activate

# 2. Install Pipeline Dependencies
pip install fastapi uvicorn sqlalchemy aiosqlite python-multipart opencv-python ultralytics torch torchvision pillow python-dotenv aiofiles

# 3. Formally Lock Requirements
pip freeze > requirements.txt
```

### 2. Frontend Configuration
In a separate terminal, navigate into the frontend folder.

```shell
cd frontend

# Install the Node Modules
npm install 
npm install axios lucide-react react-router-dom
```

---

## 🚀 Running the Project

To test the application naturally, you need two terminals open concurrently.

**Terminal 1 — Booting the AI API Engine (from root):**
```shell
# Make sure your virtual environment is active!
.\venv\Scripts\Activate.ps1

# Spin up the FastAPI Core
uvicorn backend.main:app --reload --port 8000
```
*The backend API will listen on `http://localhost:8000`.*

**Terminal 2 — Booting the React Client (from frontend/):**
```shell
cd frontend

# Start the Vite Hot-Reloading UI Server
# Note: On some Windows terminals running in the background, you may need to export CI=true first so the server doesn't force-close expecting standard input.
npm run dev
```
*The React UI will listen natively on `http://localhost:5173`.*

---

## 🧠 System Architecture Notes

- **AI Core (`backend/ai/`)**: The `detect_yolo.py` automatically dials into Ultralytics API to silently pull and cache the `yolov8n.pt` payload directly onto your machine if it's missing. Video chunking happens in `pipeline.py`.
- **Database Architecture**: Managed dynamically using SQLAlchemy standard ORMs utilizing SQLite internally for hyper-portability.
- **Vite Stability on Windows**: If Vite instantly crashes with `Exit Code 1`, force execution in CI mode via powershell: `$env:CI="true"; npm run dev`.
