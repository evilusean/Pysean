import torch
import sys
import time

def test_gpu():
    print("\nTesting GPU Access:")
    print("-" * 20)
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"CUDA version: {torch.version.cuda}")
        print(f"GPU device count: {torch.cuda.device_count()}")
        print(f"GPU device name: {torch.cuda.get_device_name(0)}")
        
        # Test CUDA computation
        x = torch.rand(5,3)
        print("\nTesting CUDA computation:")
        print(x.cuda())
    else:
        print("No GPU available!")

if __name__ == "__main__":
    test_gpu()
    
    # Keep container running
    print("\nContainer is running. Use Ctrl+C to stop.")
    while True:
        time.sleep(1)