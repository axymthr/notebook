name := "Guidebook"

version := "1.0"

scalaVersion := "2.11.8"

resolvers += "Lightbend Repository" at "http://repo.typesafe.com/typesafe/releases/"

libraryDependencies ++= Seq(
  "com.typesafe.akka" %% "akka-actor" % "2.4.8"
)
