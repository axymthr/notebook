# Read

Blog - [K3S with MetalLB on Multipass VMs](https://blog.kubernauts.io/k3s-with-metallb-on-multipass-vms-ac2b37298589)

Updated version of code at [](https://github.com/kubernauts/bonsai) with lots of other integration pieces

Hopefully this gets around the microk8s limitation of metallb not working on Mac.

```
➜  bonsai git:(master) ./deploy-bonsai.sh
How many worker nodes do you want?(default:2) promt with [ENTER]:
How many cpus do you want per node?(default:2) promt with [ENTER]:
How many gigabyte memory do you want per node?(default:4) promt with [ENTER]:
How many gigabyte diskspace do you want per node?(default:10) promt with [ENTER]:
Launched: k3s-master    
Launched: k3s-worker1                                                           
Launched: k3s-worker2    
exporting KUBECONFIG file from master node
[Info] setting KUBECONFIG=~/code/learn/read/multipass-metallb/bonsai/k3s.yaml
NAME          STATUS     ROLES                  AGE   VERSION
k3s-master    Ready      control-plane,master   24s   v1.20.4+k3s1
k3s-worker1   Ready      node                   11s   v1.20.4+k3s1
k3s-worker2   NotReady   node                   4s    v1.20.4+k3s1
are the nodes ready?
[FINISHED]

export KUBECONFIG=~/code/learn/blogs/multipass-metallb/bonsai/k3s.yaml

```

# Getting started with Knative

Original post: https://itnext.io/knative-kubernetes-native-paas-with-serverless-a1e0a0612943

deploy Knative-Serving
deploy Gloo

Let’s create an autoscaling Knative Service (kservice) and route some traffic to it.

```
apiVersion: serving.knative.dev/v1alpha1
kind: Service
metadata:
 name: helloworld-go
 namespace: default
spec:
 template:
   spec:
     containers:
       - image: gcr.io/knative-samples/helloworld-go
         env:
           - name: TARGET
             Value: Knative user
```

```
glooctl proxy url --name knative-external-proxy

```


```

kubectl get route knative-app  --output=custom-columns=NAME:.metadata.name,URL:.status.url
```