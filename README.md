# Gitlab Release Notes Generator

Generate a changelog listing all merged requests since the last release of the repository.

## Do it online: 
[![https://img.shields.io/badge/back4app-run-brightgreen](https://img.shields.io/badge/back4app-run-brightgreen)](https://gitlabreleasenotes-thomasvuillaume.b4a.run/)

## Alternative
If the back4app is down for any reason, you may try on mybinder:
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
