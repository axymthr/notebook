# Run through of Spring Boot with Docker guide (with changes to make cmds pass)
Run through https://spring.io/guides/gs/spring-boot-docker/
## Setup
- Latest zip from start.spring.io
- Gradle
- JDK 17
- Intellij

## Steps
### Local build
```shell
./gradlew build && java -jar build/libs/spring-docker-0.0.1-SNAPSHOT.jar
```
### HTTP request
```
###
GET http://localhost:8080/

HTTP/1.1 200

Hello World from Docker
```
### Basic Dockerfile with non-root user
```dockerfile
FROM mcr.microsoft.com/openjdk/jdk:17-ubuntu
RUN addgroup spring && adduser --ingroup spring spring
ARG JAR_FILE=build/libs/*.jar
COPY ${JAR_FILE} app.jar
ENTRYPOINT ["java","-jar","/app.jar"]
```
### Docker build commands
```shell
docker build -t springio/spring-docker .
docker run -p 8080:8080 springio/spring-docker
```
### Layered Dockerfile with exploded jar
```shell
mkdir -p build/dependency
cd build/dependency 
jar -xf ../libs/spring-docker-0.0.1-SNAPSHOT.jar
cd -
```
```dockerfile
FROM mcr.microsoft.com/openjdk/jdk:17-ubuntu
RUN addgroup spring && adduser --ingroup spring spring
ARG DEPENDENCY=build/dependency
COPY ${DEPENDENCY}/BOOT-INF/lib /app/lib
COPY ${DEPENDENCY}/META-INF /app/META-INF
COPY ${DEPENDENCY}/BOOT-INF/classes /app
ENTRYPOINT ["java","-cp","app:app/lib/*","com.example.springdocker.SpringDockerApplication"]
```
