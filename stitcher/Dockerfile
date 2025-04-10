FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only proto files first so Docker cache can work
COPY app/proto ./proto

# Compile .proto to Python stubs
RUN python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. ./proto/stitcher.proto

# Now copy the full app code
COPY app/ .

CMD ["python", "start_servers.py"]
