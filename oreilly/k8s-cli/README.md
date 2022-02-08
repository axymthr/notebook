### Steps
Starter template at https://github.com/codementor/k8s-cli
origin	git@github.com:codementor/k8s-cli

```
git clone https://github.com/codementor/k8s-cli

make cli
go run cmd/kubectl-example/main.go
go run cmd/kubectl-example/main.go version

make cli-install
kubectl example version
kubectl example resources
kubectl example pod list
add pod list code using direct object references

kubectl example pod list2
add pod list code using the rest client

kubectl example pod add an-attempt
adding a pod

# Add code changes in pkg/example/cmd/pod_list.go
go run cmd/kubectl-example/main.go pod list

kubectl create deployment nginx --image=nginx
deployment.apps/nginx created

kubectl scale deployment nginx --replicas=3
deployment.apps/nginx scaled

make cli-install
kubectl example pod list
Pod nginx-f89759699-c695x in Namespace: default
Pod nginx-f89759699-pq89r in Namespace: default
Pod nginx-f89759699-zng2w in Namespace: default

go run cmd/kubectl-example/main.go pod list --status=true
pod nginx-f89759699-c695x in namespace: default, status: Running
pod nginx-f89759699-pq89r in namespace: default, status: Running
pod nginx-f89759699-zng2w in namespace: default, status: Running

go run cmd/kubectl-example/main.go pod list --status=f
Pod nginx-f89759699-c695x in Namespace: default
Pod nginx-f89759699-pq89r in Namespace: default
Pod nginx-f89759699-zng2w in Namespace: default

make cli-install
kubectl example pod list --status=true
pod nginx-f89759699-c695x in namespace: default, status: Running
pod nginx-f89759699-pq89r in namespace: default, status: Running
pod nginx-f89759699-zng2w in namespace: default, status: Running

kubectl example pod list --status=t
pod nginx-f89759699-c695x in namespace: default, status: Running
pod nginx-f89759699-pq89r in namespace: default, status: Running
pod nginx-f89759699-zng2w in namespace: default, status: Running

kubectl example pod list --status=f
Pod nginx-f89759699-c695x in Namespace: default
Pod nginx-f89759699-pq89r in Namespace: default
Pod nginx-f89759699-zng2w in Namespace: default

kubectl example pod list
pod nginx-f89759699-c695x in namespace: default, status: Running
pod nginx-f89759699-pq89r in namespace: default, status: Running
pod nginx-f89759699-zng2w in namespace: default, status: Running

go run cmd/kubectl-example/main.go pod list2
RESTifarian technique
Pod nginx-f89759699-c695x in Namespace: default
Pod nginx-f89759699-pq89r in Namespace: default
Pod nginx-f89759699-zng2w in Namespace: default

make cli-install
kubectl example pod list2
RESTifarian technique
Pod nginx-f89759699-c695x in Namespace: default
Pod nginx-f89759699-pq89r in Namespace: default
Pod nginx-f89759699-zng2w in Namespace: default

# Add code changes in pkg/example/cmd/pod_add.go

go run cmd/kubectl-example/main.go pod add incredible
Pod incredible created with rev: 9414
kubectl get pods
NAME                    READY   STATUS    RESTARTS   AGE
incredible              1/1     Running   0          18s

make cli-install
kubectl example pod add it-just-gets-better
Pod it-just-gets-better created with rev: 9542

kubectl get pods
NAME                    READY   STATUS    RESTARTS   AGE
incredible              1/1     Running   0          60s

```
