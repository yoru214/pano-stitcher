# 📸 Pano Stitcher

A simple and lightweight image stitching tool and API for creating panoramas or virtual tours from multiple images.

Supports:
- 🛰️ HTTP and gRPC server (via FastAPI + gRPC)
- 🧩 Local CLI stitching without a server
- 🪄 Easy deployment to Google Cloud Run

---

## 🚀 Installation (Local / Server)

### 🛠 Requirements
- Python 3.10+
- Docker
- (Optional for local stitching) `opencv-python-headless`, `pillow`

### 🔧 Steps

```bash
# Clone the repo
cd pano-stitcher

# Build and run the API (HTTP + gRPC)
docker compose up --build
```

- Server will be available at:
  - HTTP: `http://localhost:8000/stitch`
  - gRPC: `localhost:50051`
  - Swagger UI: `http://localhost:8000/docs`

---

## ☁️ Deploy to Google Cloud Run

### 📦 Enable required APIs:
- Cloud Run
- Artifact Registry
- Cloud Build

### 📤 Build and deploy

```bash
# Build and push container to Google Artifact Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/pano-stitcher

# Deploy to Cloud Run
gcloud run deploy pano-stitcher \
  --image gcr.io/YOUR_PROJECT_ID/pano-stitcher \
  --platform managed \
  --allow-unauthenticated \
  --memory 1Gi --port 8000
```

> ✅ Expose port 50051 separately for gRPC if needed, or add gRPC proxy.

---

## 🧪 How to Use

### 📡 HTTP API

- `POST /stitch`
- `x-internal-key: dev-secret-key`
- `form-data`: upload `images[]`
- `?format=webp|jpeg`

Swagger UI: `http://localhost:8000/docs`

---

### ⚡ gRPC

- Method: `stitcher.Stitcher/Process`
- Input: `StitchRequest` with `images`, `format`, `key`

Use tools like:
- `grpcurl`
- BloomRPC

You may also use the included Python client:

```bash
python process.py 
```

---

## 🧱 Local-Only Mode (No Server)

You can stitch panoramas locally from the command line without using the server.

### 🗂 Folder Structure

```
images/
├── src/       # source images
└── output/    # stitched results
```

### 🧪 Run

```bash
python process.py --local
```

You'll be prompted to:
- Choose output filename
- Choose format (`webp` or `jpeg`)

---

## 🧬 Protobuf Code Generation

Only needed if you modify `stitcher.proto`:

```bash
python -m grpc_tools.protoc \
  -I./app/proto \
  --python_out=./app \
  --grpc_python_out=./app \
  ./app/proto/stitcher.proto
```

Make sure `stitcher_pb2.py` and `stitcher_pb2_grpc.py` are generated inside the `app/` folder.

---

## 📦 Required Python Packages (for local mode)

```bash
pip install grpcio grpcio-tools opencv-python-headless pillow
```

---

## 📁 Project Structure

```
pano-stitcher/
├── docker-compose.yml
├── stitcher/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py
│       ├── grpc_server.py
│       ├── start_servers.py
│       ├── process.py
│       ├── proto/
│       │   └── stitcher.proto
│       ├── stitcher_pb2.py
│       ├── stitcher_pb2_grpc.py
│       └── images/
│           ├── src/
│           └── output/
```

---

## 📝 License

This project is licensed under the MIT License — free for personal and commercial use. See the [LICENSE](LICENSE) file for full terms.
