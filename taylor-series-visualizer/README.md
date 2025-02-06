# Taylor Series Visualizer

## Overview

This tool reads a user-provided mathematical function in terms of $x$ and calculates its Taylor polynomial up to the 10th degree. The original function is plotted alongside the current Taylor polynomial.


## Features
- A graph that displays both the user-provided function and the current Taylor polynomial
- A slider to control the degree of the Taylor polynomial
- The grpah also supports zooming and panning

## Installation
1. Clone repository
```bash
git clone https://github.com/wgreenwood4/portfolio.git
cd taylor-series-visualizer
```
2. Install dependencies
```bash
pip install -r requirements.txt
```
3. Run script
```bash
python taylor-series-visualizer.py
```

## Usage
Simply run the script to be prompted to enter a function. Here is an example of how to visualize the Taylor Series for $e^x$.
```bash
python .\taylor-series-visualizer.py
Enter a mathematical function in terms of x: e^x
```
From here, the tool will launch, and the user can use the slider to visualize the construction of the Taylor Series.

***Note:*** The current version of this tool does not support functions with domain restrictions (e.g. $\frac{1}{x}$, $\ln(x)$, $\sqrt{x}$).

To visualize a different function, simply close the tool and run the script again with a new function.