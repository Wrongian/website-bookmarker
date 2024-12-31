# Bookmarking Thing

Encrypted bookmark/link manager(for my convenience because I didn't like the solutions out there).\
Very 5 sec thrown together UI since im the only one using it :3

## How it looks like

Main Page:
![Imgur](https://i.imgur.com/cD1NM2d.png)
Inside a bookmark category:
![Imgur](https://i.imgur.com/tbifkkQ.png)
![Imgur](https://i.imgur.com/9RbwNTy.png)
Searching:
![Imgur](https://i.imgur.com/VXGtGJG.png)

## How to Install

1. Get Python 3.10
2. Install pipenv on that specific ver of python
3. Download the entire repo off github
4. While in this folder, run `pipenv  install` or `py -3.10 -m pipenv install`
5. Done!

## How to Run

1. You can change the settings in resources.py file, (settings later maybe)
2. Make sure debug mode is set to `False`
3. click on the run.bat do `pipenv run python app.py` or `py -3.10 pipenv run python app.py`

## How to Load Backups

1. Replace the current db with the backup with the correct db file name(can be found in the configs)

## How to Update

1. Download the new files from github
2. Replace everything in the folder with the new files(might have to change the config file again)
3. Done!
