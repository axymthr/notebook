Use csr-gen.go to generate a certificate signing request to generate a new certificate
```
go run csr-gen.go client <user-name>;
```
This creates files called client-key.pem and client.csr. You then can run the create-cert.sh script to create and download a new certificate

you can use custom resource definitions (CRDs) to enable users to dynamically create and allocate new namespaces using the kubectl tool. 
After you have tooling to enable the allocation of namespaces, you also need to add tooling to reap namespaces when their TTL has expired. Again, you can accomplish this with a simple script that examines the namespaces and deletes those that have an expired TTL.

You can build this script into a container and use a ScheduledJob to run it at an interval like once per hour.
