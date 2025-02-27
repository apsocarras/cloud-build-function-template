https://stackoverflow.com/questions/10065526/github-how-to-make-a-fork-of-public-repository-private



#### Initialize from public 

```bash 
export PUBLIC_REMOTE="git@github.com:apsocarras/cloud-build-function-template.git"
export PRIVATE_REMOTE="git@github.com:WorldCentralKitchen/cloud-build-function-template.git"

## Mirror push a bar clone of the public to the private remote 
git clone --bare $PUBLIC_REMOTE public_bare
cd public_bare
git push --mirror $PRIVATE_REMOTE
cd ..
rm -rf public_bare
```

#### Working with the private repo locally

```bash 
git clone $PRIVATE_REMOTE <private_repo_name>
cd <private_repo_name>
# ... make changes 
git commit  
git push origin main 
```

#### Add public remote as tracking, and pull updates 

```bash 
cd <private_repo_name>
git remote add public $PUBLIC_REMOTE 
git pull public main 
git push origin main 
```

#### Updates public from private 

![fork](static/assets/image3.png)

Use the GitHub UI to make a fork of the public repo. We push our private code to this fork...

```bash 
export PUBLIC_FORK="git@github.com:WorldCentralKitchen/cloud-build-function-template-public-fork.git"
git clone $PUBLIC_FORK  <public_fork_repo_name>
cd <public_fork_repo_name>
git remote add <private_repo_name> $PRIVATE_REMOTE
git checkout -b <name_of_PR>
git pull <pritvate_repo_name> main 
git push origin <name_of_PR>
```
...Then create a PR in the GitHub UI to merge changes from our fork into the original public remote.  

(Our public forks acts an intermediary to "their" public fork).
