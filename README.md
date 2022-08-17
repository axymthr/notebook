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
