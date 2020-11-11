kill `netstat -nlp | grep :80 | awk '{print $7}' | awk -F"/" '{ print $1 }'` 
cd ./www 
python3 -m http.server 80 &
cd ../
pipenv run uvicorn main:app --reload