cd ./www 
python3 -m http.server 80 &
cd ../
uvicorn main:app --reload