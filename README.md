# gitlab-release-notes webapp

Flask app deployed on heroku at https://gitlab-release-notes.herokuapp.com/


## Instructions

The flask app can be run and tested separately by running
```bash
python run.py
```

### Install Heroku

https://devcenter.heroku.com/articles/getting-started-with-python#set-up


### Build and test locally:

Install requirements:
```
pip install -r requirements.txt
```

Start app:
```
heroku local
```

### Push changes

```
git remote add heroku https://git.heroku.com/gitlab-release-notes.git
```

```
git add
git commit -m " "
git push heroku master
heroku open
```


## Install and run locally

To install: 
```
pip install gitlab_release_notes
```

Then run:
```
gitlab-release-notes --help
```

## Heroku 

Heroku is setup in the `heroku` branch.
- make a new release of `gitlab_release_notes`
- manually deploy from https://dashboard.heroku.com/apps/gitlab-release-notes/deploy/github choosing the heroku branch


## Install and run locally

To install: 
```
pip install gitlab_release_notes
```

Then run:
```
gitlab-release-notes --help
```

## Heroku 

Heroku is setup in the `heroku` branch.
- make a new release of `gitlab_release_notes`
- manually deploy from https://dashboard.heroku.com/apps/gitlab-release-notes/deploy/github choosing the heroku branch
