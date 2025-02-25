## cloud-build-function-template

This is a template you can use to create a Cloud Function in GCP with CI/CD through the managed service Google Cloud Build. Cloud Build is an alternative deployment method to GitHub Actions, which can also publish to Cloud Functions. This deployment method can be incorporated with other CI/CD checks via GitHub Actions (as is demo'd in this template).  

### Prerequisites 

* Install Git
* Install uv 
* Install gcloud CLI and authenticate (`gcloud auth login`)
* Install GitHub CLI and authenticate (e.g. `gh auth login`, or [setup SSH](https://github.com/github/docs/blob/main/content/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent.md))
* Install the [Google Cloud Build GitHub App](https://github.com/marketplace/google-cloud-build)
    * Save the installation ID of the cloud build app located at: `https://github.com/settings/installations` (you will need to provide this parameter when prompted in the next step )
* Create a GitHub [personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)

## Setup 

#### 1. Create a new project with this cookiecutter 

```bash
uvx https://github.com/apsocarras/cloud-build-function-template.git 
```
The above command will open a CLI interface for you to setup your own project based off this template. The CLI will prompt you for the parameters contained in `cookiecutter.json` to generate `scripts/setup.sh`.

#### 2. Run `scripts/setup.sh`

```bash
source scripts/setup.sh
```
Be sure to review the script before running to ensure the parameters were filled out as you intended. The post install hook for cookiecutter will print out the values you entered for you to confirm. `hooks/pre_gen_project.py` contains some checks to validate inputs (won't be exhaustive). 

The setup script will perform the following steps: 

* Connect your github repository to cloud build. 
* Create an Artifact Registry repository for storing your app's docker image 
* Add the `cloudbuild.builds.builder` permission to the default cloud build service account for the project (if it doesn't have it already)
* Create a build trigger in Cloud Build. 

## Workflow 

Based on the build trigger defined in the setup, the cloud function will deploy whenever a new commit is made to main (provided that all tests pass). 

## Secrets Management