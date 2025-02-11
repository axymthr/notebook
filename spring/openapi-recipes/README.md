## Using Spring with OpenAPI
Code from [Using Spring with OpenAPI](https://www.youtube.com/watch?v=dkiJbJhNToA)
Github: https://github.com/dsyer/openapi-demo

- Uses `smallrye` to generate openapi.yml as part of the build. Check the build plugin config `generate-schema` goal in pom.xml.
  - Generates openapi.json/yaml in target/generated dir from the existing Spring Boot endpoints
- Uses `openapi-generator-maven-plugin` to generate code from openapi.yml file. Needs a bunch of config to generate the desired code implementation.
  - Contains generator config for both spring and Java code.
  - Needs `swagger-annotations` and `jackson-databind` deps.
  - Generates a whole project with a bunch of all possible boilerplate and build scripts of all sorts.
  - Only generates an interface which needs to be implemented. Generated interface can get resynced and added to the classpath.
- Uses `springdoc-openapi-starter-webmvc-api` is used to expose a dynamic JSON API spec of endpoints on /v3/api-docs when the app starts
- TODO: Instead of using swagger-annotations should have tried to use springdoc library annotations.

I'm not really sold on the openapi-generator approach. It just introduces unnecessary boilerplate, complexity, and lots of messy build settings for not that much value. Definitely don't need it for server side code. Even when I've used it in the past it just made things more complex even for client generation. 
