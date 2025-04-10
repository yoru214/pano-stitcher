# 🤝 Contributing to Pano Stitcher

Thank you for considering contributing to **Pano Stitcher**! This project welcomes contributions to improve its image stitching capabilities, performance, documentation, and more.

---

## 🛠 Local Development Setup

Before contributing, set up the project locally:

### Requirements
- Python 3.10+
- Docker & Docker Compose

### Install dependencies for local CLI use:
```bash
pip install grpcio grpcio-tools opencv-python-headless pillow
```

### Run the server:
```bash
docker compose up --build
```

- HTTP: `http://localhost:8000/stitch`
- Swagger: `http://localhost:8000/docs`
- gRPC: `localhost:50051`

---

## ✍️ How to Contribute

### 1. Fork and Clone
```bash
git clone https://github.com/YOUR_USERNAME/pano-stitcher.git
cd pano-stitcher
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes
- Follow the project structure and style
- Add tests if applicable
- Update documentation if needed

### 3. Commit and Push
```bash
git commit -m "✨ Add cool feature"
git push origin feature/your-feature-name
```

### 4. Open a Pull Request
- Base branch: `main`
- Include a clear description and screenshots if helpful

---

## 🧪 Testing

Run the local stitching script to test core functionality:
```bash
python process.py
```
You’ll be prompted to:
- Read from `images/src`
- Save result to `images/output`

Use `--local` to force offline OpenCV stitching without gRPC:
```bash
python process.py --local
```

---

## 🐛 Reporting Bugs

Please include:
- ✅ Clear reproduction steps
- 🖼 Sample image(s) if applicable
- 📋 Environment details (OS, Python version, browser, etc.)

You may open a GitHub issue or contact the maintainer directly.

---

## 🧬 Updating gRPC / Protobuf

If you update `stitcher.proto`, regenerate the gRPC bindings:
```bash
python -m grpc_tools.protoc \
  -I./app/proto \
  --python_out=./app \
  --grpc_python_out=./app \
  ./app/proto/stitcher.proto
```

---

## 💬 Contact
Maintainer: [Emmanuel Zerna](mailto:emzer214@gmail.com)

Thank you for your interest in improving Pano Stitcher! 🚀
