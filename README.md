## cloud-build-function-template

This is a CookieCutter template you can use to create a Cloud Function in GCP with CI/CD through Google Cloud Build. 

You can find more about the tools used in [`tools`](tools.md).



### Usage 

First ensure that you have the prerequisites checked off in [`prerequisites.md`](prerequisites.md) and have the outputs saved. 

#### 1. Create a new local project

```bash
uvx https://github.com/apsocarras/cloud-build-function-template.git 
```
The above command will open a CLI interface for you to setup your own project based off this template. It will prompt you for the parameters contained in `cookiecutter.json`.


#### 2. Initialize your new local project 

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

#### 3. Run `scripts/setup_script.py`

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

* If you selected yes to `publish_to_pypi`, another workflow `release_pypi.yaml` is included. `v`-tagged commits will be published to PyPI and your package version number will be updated dynamically via `setuptools-scm`