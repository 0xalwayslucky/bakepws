# Bakepws - Baking Passwords With Ease
**Bakepws.py** creates a password-list based on the words supplied via input file.
I created this tool to generate a lot of passwords for a specific target with minimum
effort.
## Documentation
### What is it doing?
```
Without any modifications all words of the input file will be combined until no more
variations are left and printed to standard output.

-i      Specify an input file. Only the first word of the line will be considered, so
        one word per line.

-r      When supplying a hashcat rule bakepws.py uses hashcat to generate modified
        lists for each word before combining the words.

-a      Using the -a (all) option will - in addition to combining the words - 
        also include the words itself and combinations that do not use all words of the 
        supplied input file. When specifying this -c, --min and --max will be ignored.
        
        Example:
        > Input file consists of 5 words
        > Output will consist of words in the range of 0 to 4 combinations, meaning
          each word is combined with 0, 1, 2, 3 and 4 other word(s) and then printed to
          output

-o      Specify an output file. With no output file specified, standard output will be
        used.
       
-c      Specify the exact amount of combinations. n means one word combined with n others.
        When specifying this, --min and --max will be ignored.
        
--min   Sepcify the amount of minimum combinations. 0 means no combinations will be made.
        When specifying --min, --max will default to maximum possible length.

--max   Specify the amount of maximum combinations. n means one word combined with n 
        others. When specifying --max, --min will default to 0.

--cat   Specify a custom hashcat path. On default /bin/hashcat and /usr/bin/hashcat
        will be checked.
```
_Note: Hashcat has to be installed in order to use the -r option. More about [hashcat](https://github.com/hashcat) and [hashcat rules](https://hashcat.net/wiki/doku.php?id=rule_based_attack)_

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
      -c:     Combine exactly n word(s)
   --min:     Specify minimum amount of combinations
   --max:     Specify maximum amount of combinations
   --cat:     Specify a custom hashcat path

Examples:
python3 bakepws.py -i examples/dough.txt
python3 bakepws.py -i examples/dough.txt -r examples/recipe.rule -a
python3 bakepws.py -i examples/dough.txt -r examples/recipe.rule -o examples/cake.txt
```
## Disclaimer
All scripts should be used for authorized penetration testing purposes only. Any misuse will not be the responsibility of the author.
