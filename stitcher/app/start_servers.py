import multiprocessing
import uvicorn
import signal
import sys
from grpc_server import serve_grpc

def start_http():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)

def start_grpc():
    serve_grpc()

def shutdown(signum, frame):
    print("\n[Shutdown] Caught signal, exiting...")
    sys.exit(0)

if __name__ == "__main__":
    # Register signal handlers for Docker/Kubernetes or local Ctrl+C
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    # Start HTTP and gRPC as separate processes
    p1 = multiprocessing.Process(target=start_http)
    p2 = multiprocessing.Process(target=start_grpc)

    try:
        p1.start()
        p2.start()
        print("[INFO] HTTP (FastAPI) and gRPC servers started.")

        # Wait for both to finish
        p1.join()
        p2.join()

    except KeyboardInterrupt:
        print("[INFO] KeyboardInterrupt detected. Terminating servers...")
        p1.terminate()
        p2.terminate()
        p1.join()
        p2.join()
        print("[INFO] Servers shut down cleanly.")
