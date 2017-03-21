# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* A small attempt to make a compiler, which compiles JAVA language. The compiler is implemented in PYTHON and uses MIPS as the base language.
* It is done for a course CS335A - Compiler design under Prof. Amey Karkare, CSE dept., IITK.
* The first commit is of lexer and parser, the second one is for semantic analysis. 
### Files Description ###
**lexer.py**  : contains  the lexer part of the compiler, were token and keywords are defined. Lexical analysis is the first phase of a compiler. It takes the modified source code from language preprocessors that are written in the form of sentences. The lexical analyzer breaks these syntaxes into a series of tokens, by removing any whitespace or comments in the source code.

**testLexer.py** : code to check if the tokens are being generated as needed.

**parser.py**  : contains the grammar of JAVA language and actions which help in generating the parse tree which will be usefull in the next phase of compiler. Its done using lists data structure in Python.

 **testParser.py**  : code to check if the compiler is parsing the input. the parser obtains a string of tokens from the lexical analyser, and verifies that the string can be generated by the grammar for the source language. The parser returns any syntax error for the source language.

**parsetab.py** : This file is automatically generated, do not edit. 

**semanticAnalysis.py** : Semantic analysis, also context sensitive analysis, is a process in compiler construction, usually after parsing, to gather necessary semantic information from the source code. It usually includes type checking, or makes sure a variable is declared before use and thus report errors which are not easily detected during parsing phase.

**semanticTest.py**: code to test semantic phase and simultaneously enters the (key,value) pairs in symbol table.

**stack.py** : implemented a stack to perform certain actions while dealing with the symbol table. 

**symbolTable.py** : implementation of symbol table using 'lists' data-structure. It has 3 methods insert(), lookup() and lookupCurrentScope(). lookup() searches for the symbol in the current scope if found, returns it else looks in the scope of the parent's scope, whereas lookupcurrent scope searches the symbol in the current scope itself.

### How do I get set up? ###

* initially, cd to folder where the files are.
* python semanticAnalysis.py 'file_name'
* Symbol table details in symbolTable.text

### Contribution  ###

* Prashant kumar(11525) and Nishanth Gunupudi(11289)

# References  :  JAVA grammar from Java SE Specifications, Java Language Specification, Oracle.

### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact