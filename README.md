# Bakepws - Baking Passwords With Ease
**Bakepws.py** creates a password-list based on the words supplied via input file.
I created this tool to generate a lot of passwords for a specific target with minimum
effort.
## Documentation
### What is it doing?
```
Without any modifications all words of the input file will be combined until no more
variations are left and printed to standard output.
```

### How do I use it?
```
-i      Specify an input file. Only the first word of the line will be considered, so
        one word per line.
```

### What do you mean, modifications?!
```
-r      When supplying a hashcat rule bakepws.py uses hashcat to generate modified
        lists for each word before combining the words.
```
_Note: Hashcat has to be installed in order to use this option. More about [hashcat](https://github.com/hashcat) and [hashcat rules](https://hashcat.net/wiki/doku.php?id=rule_based_attack)_

### Just give me everything you have!
```
-a      Using the -a (all) option will - in addition to combining the words - 
        also include the words itself and combinations that do not use all
        words of the supplied input file.
        
        Example:
        > Input file consists of 5 words
        > Output will consist of words in the range of 0 to 4 combinations, meaning
          each word is combined with 0, 1, 2, 3 and 4 other word(s) and then printed to
          output
```

### What do I do with the output?
```
-o      Specify an output file. With no output file specified, standard output will be
        used.
```

### It doesn't find my Cat! Wat now?
```
--cat   Specify a custom hashcat path. On default /bin/hashcat and /usr/bin/hashcat
        will be checked.
```

### Do you have sample output for me?
```
> python3 bakepws.py -i examples/dough.txt -r examples/receipe.rule -o examples/cake.txt

examples/
> dough.txt     ->   input file
> receipt.rule  ->   hashcat rule
> cake.txt      ->   output file
```

## Usage
```
Creating a password-list with ease. 

Usage:
python3 bakepws.py [OPTIONS] -i <input-file>

With no output file, print to standard output

      -i:     Specify an input file
      -r:     Specify a hashcat rule
      -o:     Specify an output file
      -a:     Print all words and combinations
   --cat:     Specify a custom hashcat path

Examples:
python3 bakepws.py -i examples/dough.txt
python3 bakepws.py -i examples/dough.txt -r examples/recipe.rule -a
python3 bakepws.py -i examples/dough.txt -r examples/recipe.rule -o examples/cake.txt
```
## Disclaimer
All scripts should be used for authorized penetration testing purposes only. Any misuse will not be the responsibility of the author.
