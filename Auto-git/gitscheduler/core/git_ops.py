import git

def execute_git(repo_path, message, branch):
    repo = git.Repo(repo_path)

    if not repo.is_dirty(untracked_files=True):
        return "no_changes"

    repo.git.add(A=True)
    repo.index.commit(message)
    repo.remote().push(branch)

    return "completed"
