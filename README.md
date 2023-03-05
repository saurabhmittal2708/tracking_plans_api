# tracking_plans_api
Repo for API and UI of tracking plans take home assignment


# Setup
## Create virtual environment
```
python -m venv <venv_name>
<venv_name>\Scripts\activate
```

## Install dependencies
```
pip install -r requirements.txt
```

## Set up aws credentials
Setup AWS access key, secret key, and region in `.env`

## Start flask server
```
set FLASK_APP = app.py
flask run
```

Go to `http://localhost:5000/tracking_plans` and voila!

## Load up UI
Open up `ui/index.html` in a browser and you are good to go
