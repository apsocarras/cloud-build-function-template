from github import Github


def check_github_pat(github_author: str, github_pat: str):
    g = Github(github_pat)
    authenticated_user = g.get_user().login
    if authenticated_user != github_author:
        raise RuntimeError(
            f"GitHub PAT doesn't match provided github account {github_author}"
        )


def check_github_repo(github_author: str, project_name: str, github_pat: str):
    # Authenticate with GitHub using the PAT
    g = Github(github_pat)

    # Fetch the repository
    repo_full_name = f"{github_author}/{project_name}"
    try:
        repo = g.get_repo(repo_full_name)
        return repo
    except Exception as e:
        raise Exception(
            f"Repository '{repo_full_name}' not found or access denied: {e}."
        )
