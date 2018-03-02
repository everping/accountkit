## Description
This application is an implementation of the Facebook Account Kit, for the purpose of testing. It's written in [Flask Framework](http://flask.pocoo.org/) and deployed on [Heroku](https://heroku.com/).

## Usage
- Replace `APP_ID` and `ACCOUNT_KIT_APP_SECRET` in `main_app` by your values
- `pip install -r requirements.txt`
- `python main_app.py`

## Heroku deploying
```shell
heroku create
git add *
git commit -m "update code"
git push heroku master
```

## Live demo
https://accountkit.herokuapp.com/

# Credits
- https://github.com/devries/accountkit-bottle
