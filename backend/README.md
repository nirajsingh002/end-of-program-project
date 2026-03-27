# installation

pip install -r requirements.txt

# Create conda env

conda create -n crop_env python=3.10

# activate env

conda activate crop_env

# Run backend

uvicorn main:app --reload
