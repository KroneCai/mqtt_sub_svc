# activate virtual environment
source  $(pwd)/venv/bin/activate

# install & upgrade all depends
pip install --upgrade -r requirements.txt

# show current working directory
echo "当前工作目录: $(pwd)"
cd ./app
# run uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload