---
layout: default
title: On Javascript Support
nav_order: 9
---

# On Javascript Support

## Overview  

One of the main disadvantages of Python is that is hard (impossible?) to distribute a package as a standalone application. Still I wanted to have this library usable in the browser and in apps, to open up a wide range of potential applications.  

There are several tools enabling the use of Python in the browser but most of the time they require downloading a javascript file containing the Python interpreter, plus another one for the standard library (this is the case for Brython). These files are pretty big (a few mbs) and take a while to parse. While this can be acceptable on desktop, this is going to take a while for a mobile user.  

Another possibility is to call the user's python install through system calls. Once again this approach has issues: the user needs to have python plus all the dependencies installed. This is the approach I used for [VisualMidi](https://github.com/Wally869/VisualMidi) and it's not pretty.  

That's why I decided to transpile MusiStrata using Transcrypt.  


## Transpilation, and Constraints on Code  

This section is mostly to explain the "odd" design choices in terms of code and to help other people wishing to do something similar. 

While Transcrypt is working suprisingly well as a Python-to-JS transpiler, using it means there are features I add to give up on/modify to make it usable.  

Among the problems I encountered:  
- No Enums. This is due to backwards compatibility issues: [Built in function 'super' with arguments not supported](https://github.com/QQuick/Transcrypt/issues/643)
- Errors on Operator Overloads. 2 issues here: 


## Current Status  

At the time of writing (2020-08-05):
- In the Components folder, all files are transpiling and executing successfully in the browser, with the exception of Structure.py which is still untested  
- In the Root folder, nothing has been tested yet. MidoConverter and Noteplayer will most likely be unsupported.  

This is WIP and is likely to be released in its own repo.