pushd "%~dp0"
start "" http://www.localhost:5000
py -3.10 -m pipenv run python app.py
pause