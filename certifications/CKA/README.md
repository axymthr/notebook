# CKA prep notes

## Cluster Components

### ETCDCTL

Check etcdctl version is 3

```
ETCDCTL_API=3 etcdctl version
export ETCDCTL_API=3
```

Get etcdctl cmd line flags exactly as-is from static pod manifest or `describe` command.

### Cluster Upgrade

### Static pods

## Taints, Tolerations, Node Affinity

[Well-Known Labels, Annotations and Taints](https://kubernetes.io/docs/reference/labels-annotations-taints/)

## Deployments

### Updates, Rollouts



## Networking

### Components

- Kube-dns/Core-dns - service/pod communication
- Overlay network addon plugin - pod communication
- Kube-proxy - service communication

## General tips

bash auto-completion installed check

Check num nodes in the cluster(s)

Read ques. 1st, note details in gedit then put ans together

prefix YAML file with the question number for example, 01-pod.yaml

If you don't know a question move on

Change context on each question even if you don’t need to change

### Bookmarks

https://kubernetes.io/docs/reference/kubectl/cheatsheet/

https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/



