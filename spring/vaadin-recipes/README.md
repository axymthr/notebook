# Vaadin and Spring Boot 3.1 Demo
https://www.youtube.com/watch?v=vkk6Sg0hgDA

TestContainers did not run with Rancher Desktop at all. Initially the Rancher settings were unclear. Even after setting the configuration in the docs it didn't work to detect the Docker socket.
https://java.testcontainers.org/supported_docker_environment/

Got it running fine with Colima.
Instead of the shell set the env vars in the Intellij run config. Even that needed tweaking.
```shell
export TESTCONTAINERS_DOCKER_SOCKET_OVERRIDE=/var/run/docker.sock
export TESTCONTAINERS_HOST_OVERRIDE=$(colima ls -j | jq -r '.address')
export DOCKER_HOST="unix://${HOME}/.colima/default/docker.sock"
```
`${HOME}` and the `""` throws an error in Java/Intellij. Most likely needed escape sequences `\$` etc.

For long term want to use the TestContainers desktop app or use the testconainers user properties file.

## New aspects learned
### Convention to run application for development from test class
Uses spring-dev-tools, also new test run convention [TestVaadinApplication.java](src/test/java/com/example/vaadin/TestVaadinApplication.java)

### TestContainers support

### Mock JSON placeholder data APIs for posts


### Exchange API to proxy requests

### Vaadin

# Building Full-Stack Applications in Java with Vaadin
https://www.youtube.com/watch?v=5jRwAWjMoZU

Posts app with editing

https://github.com/danvega/hello-vaadin/

# Spring Tips: Vaadin Flow and Spring Boot 3
https://www.youtube.com/watch?v=nyR-qzj7O3w
Chat app with Spring Security login

https://github.com/spring-tips/vaadin-flow-24

# Spring Tips: Hilla, a new frontend and backend framework from Vaadin
https://www.youtube.com/watch?v=ADLbkZnKjA0
Just follows some standard Getting Started from Vaadin docs
https://github.com/spring-tips/vaadin-hilla

```shell
npx @vaadin/cli init --preset hilla-quickstart-tutorial hilla-grocery-app
```
