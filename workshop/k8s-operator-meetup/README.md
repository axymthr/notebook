Operators come under following SIGs: cluster-lifecycle + api-machinery

You can use client-go, Operator SDK, Kubebuilder, or KUDO to write operators.

https://www.youtube.com/watch?v=bWc2D1NSVPQ

Kubernetes Operators - Hands on workshop

The official example uses kubebuilder 2.3.1. There are some Go dependencies missing in Kubebuilder 2.3.2 leading to errors, extra Go commands to be run

```
cd at-controller
go mod init cnat
export GO111MODULE=on
kubebuilder init --domain awkshwayrd.dev
go get github.com/go-logr/logr@v0.1.0
go get github.com/onsi/gomega@v1.8.1
go get github.com/onsi/ginkgo@v1.11.0
go get k8s.io/api/core/v1@v0.17.2
kubebuilder create api --group cnat --kind At --version v1alpha1
kubebuilder version
kubectl apply -f config/samples/cnat_v1alpha1_at.yaml
```



Kubebuilder internally uses controller-gen to generate scaffolding code based on comment markers.

```
make manifests
# kubectl kustomize config/crd | kubectl apply -f - # newer version
# Install CRD
make install
# Run controller locally while pointing to kube-apiserver
make run
```





https://learning.oreilly.com/scenarios/kubernetes-extensibility-develop/9781492083870/

Kubernetes Extensibility: Develop an Operator with Kubebuilder



https://olm.operatorframework.io/

OPERATOR LIFECYCLE MANAGER
The Operator Lifecycle Manager (OLM) extends Kubernetes to provide a declarative way to install, manage, and upgrade Operators on a cluster.



https://book.kubebuilder.io/

O’Reilly: Kubernetes Operators: Automating the Container Orchestration Platform

https://www.redhat.com/en/resources/oreilly-kubernetes-operators-automation-ebook



https://www.redhat.com/cms/managed-files/cl-oreilly-kubernetes-operators-ebook-f21452-202001-en_2.pdf

Kubernetes Operators book from Red Hat



https://learning.oreilly.com/library/view/programming-kubernetes/9781492047094/

Programming Kubernetes book



Golang code-generators used to implement [Kubernetes-style API types](https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md).

https://github.com/kubernetes/code-generator



https://ishankhare.dev/posts/6/

https://github.com/ishankhare07/kubebuilder-controller

https://github.com/kubernetes-sigs/controller-runtime/tree/master/examples