## cloud-build-function-template

This is a template you can use to create a Cloud Function in GCP with CI/CD through the managed service Google Cloud Build. Cloud Build is an alternative deployment method to GitHub Actions, which can also publish to Cloud Functions. This deployment method can be incorporated with other CI/CD checks via GitHub Actions.  

### Prerequisites 

* Install Git
* Install uv 
* Install gcloud CLI 
* Install GitHub CLI 
* Install [cookiecutter](https://www.cookiecutter.io) - spins up a new repository with a fresh .git history based off this template

## Setup 

#### 1. Create a new project with the cookiecutter 

```bash
uvx https://github.com/WorldCentralKitchen/cloud-build-function-template.git 
```
The above command will open a CLI interface for you to setup your own project based off this template. The CLI will prompt you for the parameters contained in `cookiecutter.json`. 

#### 2. Create a new GitHub repo and connect your local repository

#### 3. Run `scripts/setup.sh`

```bash
source scripts/setup.sh
```
Be sure to review the script's command before running to ensure the parameters were filled out correctly. The post install hook for cookiecutter will print out the values you entered for you to confirm. In future iterations, I may add validation steps for the inputs you provide.

The setup script will perform the following steps: 

* Authenticate via gcloud CLI (will open your browser)
* Connect your github repository to cloud build
* Create an Artifact Registry repository for storing your app's docker image 
* Add the `cloudbuild.builds.builder` permission to the default cloud build service account (if it doesn't already have it)
* Create a build trigger in Cloud Build. 

## Workflow 

Based on the build trigger defined in the setup, the cloud function will deploy whenever a new commit is made to main (provided that all tests pass). 

## Secrets Management