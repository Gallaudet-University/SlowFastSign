from slowfast_modules.slowfast import visualize
import os

if __name__ == "__main__":
    if not os.path.exists('dataset/phoenix2014'):
        raise FileNotFoundError("Dataset not found. Please download and place it in the 'dataset' directory. Link: https://www-i6.informatik.rwth-aachen.de/~koller/RWTH-PHOENIX/")
    
    if not os.path.exists('workdir/onnx/slowfast.onnx'):
        # Produce the visualization of the SlowFast model
        visualize()
    


