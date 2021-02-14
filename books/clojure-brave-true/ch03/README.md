

## Chapter 3 Do Things: A Clojure Crash Course

Basic code syntax

```
1
"a string"
["a" "vector" "of" "strings"]
(+ 1 2 3)
(str "It was the panda " "in the library " "with a dust buster")

(if true
  "By Zeus's hammer!"
  "By Aquaman's trident!")

(if false
  "By Zeus's hammer!"
  "By Aquaman's trident!")

(if false
  "By Zeus's hammer!")

(if true
  (do (println "Success!")
      "By Zeus's hammer!")
  (do (println "Failure!")
      "By Aquaman's trident!"))

(when true
  (println "Success!")
  "abra cadabra")

(nil? 1)

(nil? nil)

(if "bears eat beets"
  "bears beets Battlestar Galactica")

(if nil
  "This won't be the result because nil is falsy"
  "nil is falsy")

(= 1 1)

(= nil nil)

(= 1 2)

(or false nil :large_I_mean_venti :why_cant_I_just_say_large)
(or (= 0 1) (= "yes" "no"))
(or nil)

(and :free_wifi :hot_coffee)
(and :feelin_super_cool nil false)

(def failed-protagonist-names
  ["Larry Potter" "Doreen the Explorer" "The Incredible Bulk"])

(defn error-message
  [severity]
  (str "OH GOD! IT'S A DISASTER! WE'RE "
       (if (= severity :mild)
         "MILDLY INCONVENIENCED!"
         "DOOOOOOMED!")))
(error-message :mild)

93
1.2
1/5
"Lord Voldemort"
"\"He who must not be named\""
"\"Great cow of Moscow!\" - Hermes Conrad"

(def name "Chewbacca")
(str "\"Uggllglglglglglglglll\" - " name)

{}
{:first-name "Charlie"
 :last-name "McFishwich"}
{"string-key" +}
{:name {:first "John" :middle "Jacob" :last "Jingleheimerschmidt"}}
(hash-map :a 1 :b 2)

(get {:a 0 :b 1} :b)
(get {:a 0 :b {:c "ho hum"}} :b)
(get {:a 0 :b 1} :c)
(get {:a 0 :b 1} :c "unicorns?")
(get-in {:a 0 :b {:c "ho hum"}} [:b :c])
({:name "THe Human Coffeepot"} :name)

:a
:rumplestiltsken
:34
:_?
(:a {:a 1 :b 2 :c 3})
(:d {:a 1 :b 2 :c 3} "No gnomes knows homes like Noah knows")

[3 2 1]
(get [3 2 1] 0)
(get ["a" {:name "Pugsley Winterbottom"} "c"] 1)
(vector "creepy" "full" "moon")
(conj [1 2 3] 4)







```

