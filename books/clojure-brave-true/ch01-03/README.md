## Chapter 1 Getting started

Leinengen installed with sdkman, running with Java 11

### Creating a New Clojure Project

```
lein new app clojure-noob
tree clojure-noob
```



```
cd clojure-noob

lein run
```



```
lein uberjar

java -jar target/uberjar/clojure-noob-0.1.0-SNAPSHOT-standalone.jar
```



### Using the REPL

```
lein repl
clojure-noob.core=> (-main)
clojure-noob.core=> (+ 1 2 3 4)
clojure-noob.core=> (* 1 2 3 4)
clojure-noob.core=> (first [1 2 3 4])
clojure-noob.core=> (do (println "no prompt here!")
               #_=> (+ 1 3))
```



## Chapter 2 Setting up Emacs

Setup Emacs and grabbed settings from https://github.com/flyingmachine/emacs-for-clojure/archive/book1.zip

Decided to do everything in Cursive with IntelliJ though



## Chapter 3 Do Things: A Clojure Crash Course

All code in clojure_code.clj file