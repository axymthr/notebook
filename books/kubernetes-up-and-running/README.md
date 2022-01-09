```
kubectl create -f load-test-crd.yaml
kubectl get loadtests
kubectl create -f load-test-resource.yaml
```
To write a custom controller you can either:
1. Run a for loop on API server and repeatedly poll for new custom objects, however this is inefficient, or
2. Use the watch API on the API server which provides a stream of updates. via the Informer pattern exposed in the client-go library.

Admission controllers can be added to a cluster via the dynamic admission control system. A dynamic admission controller is a simple HTTP application. The API server connects to the admission controller via either a Kubernetes Service object or an arbitrary URL
To install our validating admission controller, we need to specify it as a Kubernetes ValidatingWebhookConfiguration. 
```
go run csr-gen.go <URL-for-webook>

perl -pi -e s/REPLACEME/$(base64 server.csr | tr -d '\n')/ \
admission-controller-csr.yaml

kubectl create -f admission-controller-csr.yaml
kubectl certificate approve validating-controller.default

kubectl get csr validating-controller.default -o json | \
  jq -r .status.certificate | base64 -d > server.crt
```
When the admission controller code receives a request, it contains an object of type AdmissionReview, which contains metadata about the request as well as the body of the request itself.

3 kinds of use case patterns for custom controllers:
1. Just data e.g. canary %age
2. Compilers - use the CRs as input for managing lower level objects e.g. Pods/Deployments
3. Operators - management of custom resources and additional caabilities e.g. DB administation

