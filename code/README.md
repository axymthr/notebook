The Wine Cellar application provides an example of Building a complete RESTful API in Java using JAX-RS and Jersey. Consuming these services using jQuery
https://github.com/ccoenraets/wine-cellar-java

Rename all file exts in folder
```shell
for f in *.docx.md.md; do
mv -- "$f" "${f%.docx.md.md}.md";
done
```

Move all files with number pattern in nane to numbered folder e.g. day1input.txt to day1/input.txt
```shell
for f in *.txt; 
do 
d=day$(echo $f | grep -Eo '[0-9]{1,3}); # 3 digit nos.
# OR
# d=$(echo $f | sed -E 's/(day[0-9]{1,3})input.txt/\1/'); 
# OR
# d="day${f//[^0-9]}"
mkdir $d; 
mv $f $d/input.txt;
done
```
