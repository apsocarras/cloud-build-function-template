### *Toolchain*

*[uv](https://docs.astral.sh/uv/)* is the emerging standard tool for package management, .venv management, and package publishing in the Python ecosystem. 

*[CookieCutter](https://www.cookiecutter.io/)* is a structured way of using Jinja templates to quickly make new projects according to a consistent structure.

*[GitHub Actions](https://docs.github.com/en/actions)* is GitHub's native CI/CD, allowing you to automate workflows directly from your repository. It supports a wide range of tasks, including testing, building, and deploying code, as well as integration with external services.


*[Cloud Build](https://cloud.google.com/build/docs)* is a managed CI/CD service on GCP and serves as an alternative deployment method to GitHub Actions, which can also publish to Cloud Functions. Cloud Build can be incorporated into CI/CD workflows with other checks via GitHub Actions (as is demo'd in this template).  

*[Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers)* in VS Code let you work within a docker container as your workspace. This promotes consistent dev environments across machines and users.

*[setuptools-scm](https://setuptools-scm.readthedocs.io/en/stable/)* is a plugin for the `setuptools` package build system. It automatically tags your package version numbers based on the tag of the latest commit.

#### Future Tools

*[Terraform](https://www.terraform.io/)* is a declarative infrastructure-as-code tool I *should* have utilized rather than struggle with the inconsistently-documented GCP SDKs.


*[Oh My Zsh](https://ohmyz.sh/)* is a framework to improve your UX at the terminal (tab deletion, history search). I have a very nice dev setup w/ other tools configured which I'd like to include in my Dev Containers at some point.
