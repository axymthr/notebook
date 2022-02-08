## Introduction to Serverless on Kubernetes

https://learning.edx.org/course/course-v1:LinuxFoundationX+LFS157x+3T2020/home

Install with arkade

```
arkade install openfaas
arkade info openfaas
kubectl port-forward -n openfaas svc/gateway 8080:8080
```

Zsh shell completion

```
source <(faas-cli completion --shell zsh)
```



```
faas-cli list
```

Gateway UI at http://127.0.0.1:8080/ui/ username: admin password via kubectl

```
export OPENFAAS_PREFIX=awkshwayrd
```

Need to push Docker images to Hub. Didn't figure out how to change imagePullPolicy.

Check out loki and openfaas-loki for log aggregation

#### 

```
git submodule add git@github.com:alexellis/echo-fn echo-fn
```
