# Life Simulation in Python

Basic rules of Life:  
"World" is represented as an N by N matrix. Each element in the matrix may contain 1 organism. Each organism lives, dies and reproduces according to the following set of rules:  

* If there are two or three organisms of the same type living in the elements
surrounding an organism of the same, type then it may survive.  
* If there are less than two organisms of one type surrounding one of the same type
then it will die due to isolation.  
* If there are four or more organisms of one type surrounding one of the same type
then it will die due to overcrowding.  
* If there are exactly three organisms of one type surrounding one element, they may
give birth into that cell. The new organism is the same type as its parents. If this
condition is true for more then one species on the same element then species type
for the new element is chosen randomly.  
* If two organisms occupy one element, one of them must die (chosen randomly)
(only to resolve initial conflicts).  
  
Initial matrix is loaded from an XML file with a structure following the same format as *xml/world_real.xml*.


## Minimum Python version
3.6.6

## Run an example simulation
`make run`

## Run tests
`make test`
