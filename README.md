## cloud-build-function-template

This is a CookieCutter template you can use to create a Cloud Function in GCP with CI/CD through Google Cloud Build. 

*[CookieCutter](https://www.cookiecutter.io/)* is a structured way of using Jinja templates to quickly make new projects according to a consistent structure.

*[Cloud Build](https://cloud.google.com/build/docs)* is managed CI/CD service on GCP and serves as an alternative deployment method to GitHub Actions, which can also publish to Cloud Functions. Cloud Build can be incorporated into CI/CD workflows with other checks via GitHub Actions (as is demo'd in this template).  

Before attempting to use the template, first ensure that you have the prerequisites checked off (see ***Prerequisites***).

### 1. Create a new local project

```bash
uvx https://github.com/apsocarras/cloud-build-function-template.git 
```
The above command will open a CLI interface for you to setup your own project based off this template. It will prompt you for the parameters contained in `cookiecutter.json` to generate an `.env` file (stored in `_local/.env`). 

* Be sure to give a project name and github author name which matches the repo you made initially. 

* Ensure the captured values in `_local/.env` file match what you intended to provide.



### 2. Initialize your new local project 

```bash 
cd <project-name-you-provided>
git init 
git add . 
git commit -m 'initial commit'
git tag v0.0.0 # set version here.
uv sync && source .venv/bin/activate
git remote add origin <your-repo-here>
```

Feel free to edit the default GitHub Actions in `.github/workflows`  or the `cloudbuild.yaml` file as you see fit before running the final infrastructure deployment script; push to main when finished.

```bash
git push origin main
```

### 3. Run `scripts/setup_script.py`

The setup script will perform the following steps: 

* Connect your github repository to cloud build.
* Create an Artifact Registry repository for storing your app's Docker image.
* Add the `cloudbuild.builds.builder` permission to the default cloud build service account for the project (if it doesn't have it already).
* Create a build trigger in Cloud Build.

Review the functions in `src/<your_package_slug>/cloud_infra` to see all the steps involved.

--- 

### Development Workflow

Cloud Build will redeploy the Cloud Function whenever a new commit is made to any branch matching the pattern provided in the CLI setup (provided that all tests pass). 

If you selected yes to `include_github_actions`, two default worfklows are added in `.github/workflows`: 

* `ci_test.yaml` - run linter and formatter checks + pytest tests on mac, windows, and linux containers. The default configuration is to run on commits to main, but you can modify this to target branches matching e.g. `dev` to avoid redundancies with the steps in `cloudbuild.yaml`

* If you selected yes to `publish_to_pypi`, another workflow `release_pypi.yaml` is include. `v`-tagged commits will be published to PyPI and your package version number will be updated dynamically via `setuptools-scm`
---

### *Prerequisites*

**Local Setup**:

* Install [Git](https://www.google.com/search?client=firefox-b-1-d&q=git+install) and configure [SSH](https://docs.github.com/en/authentication/connecting-to-github-with-ssh) (optional)
* Install [uv](https://docs.astral.sh/uv/getting-started/installation/)

**Cloud Services**: 

* Create an empty GitHub repository for your new project.
* Install the [Google Cloud Build GitHub App](https://github.com/marketplace/google-cloud-build) and connect it to your repository.
    * Save the installation ID of the cloud build app located at: `https://github.com/settings/installations` (you will need to provide this parameter when prompted in the CLI)
* Create a GitHub [personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) (classic) with the following permissions
    * `repo`
    * `read:org`
    * `read:user`
* Create a Google Cloud Service Account with the following IAM roles
    * `Artifact Registry Writer` 
    * `Cloud Build Editor` 
    * `Cloud Run Admin` 
    * `Cloud Run Invoker` 
    * `Secret Manager Admin` 
    * `Storage Object Creator` 
    * *Note*: In my organization, I gave the Secret Manager Admin and Storage Object Creater IAM roles to the default Cloud Build Service Account to simplify things.

Save your GitHub PAT and Service Account key .json file in a secure folder on your machine or e.g. a cloud-based password vault.