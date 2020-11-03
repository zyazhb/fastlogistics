cd ./www 
python3 -m http.server 80 &
cd ../
pipenv run uvicorn main:app --reload