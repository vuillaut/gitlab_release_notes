# Gitlab Release Notes Generator

Generate a changelog listing all merged requests since the last release of the repository.

## Do it online: 
[![Heroku](https://pyheroku-badge.herokuapp.com/?app=gitlab-release-notes)](https://gitlab-release-notes.herokuapp.com/)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/vuillaut/GitlabReleaseNotesGenerator/HEAD?labpath=generate.ipynb)


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
