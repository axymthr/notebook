# learn
All the in-progress code from whatever I'm learning or Github links to other repos

```
git submodule add git@github.com:victorrentea/structural-patterns-spring.git structural-patterns-spring
```

```
git remote add k8s-cli ~/code/k8s-cli 
git subtree add k8s-cli master --prefix=oreilly/k8s-cli --squash
```

```
git submodule add git@github.com:kodekloudhub/certified-kubernetes-administrator-course.git certifications/CKA/certified-kubernetes-administrator-course
```

Rewrite commit author for all commits in repo:
```shell
git config user.name axymthr
git config user.email mathur.aksh@gmail.com
git rebase --root --exec 'git commit --amend --no-edit --reset-author'
```
Rewrite author for last commit
```shell
git commit --amend --reset-author --no-edit
```

## Sparse checkout
```shell
git remote add origin <repository_url>
git config core.sparseCheckout true
```
Edit `.git/info/sparse-checkout` file or create `sparse-checkout` in the `.git/info` directory.
Sample from ChatGPT
```bash
echo "path/to/file1" >> .git/info/sparse-checkout
echo "path/to/directory/" >> .git/info/sparse-checkout
```
```bash
/              # Include the root directory
/docs/         # Include the 'docs' directory
/src/file1.txt # Include a specific file in the 'src' directory
```
Then run the following command to merge and update
```bash
git read-tree -mu HEAD
```
###### When to Use git read-tree -mu HEAD

git read-tree -mu HEAD can be useful if:
	•	You want to adjust the sparse-checkout configuration after the initial checkout.
	•	You’ve updated .git/info/sparse-checkout to include new paths and want to apply those changes without checking out the branch again.
In newer Git workflows, however, this command is often unnecessary. After setting up the sparse-checkout configuration and checking out the branch, Git will respect the .git/info/sparse-checkout file automatically without needing git read-tree -mu HEAD.
