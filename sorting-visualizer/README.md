# Sorting Visualizer

## Overview

This tool is capable of visualizing 7 sorting algorithms:
1. Bubble sort
1. Insertion sort
1. Selection sort
1. Shell sort
1. Merge sort
1. Quick sort
1. Heap sort

Visualizations are made using vertical bars of varying heights. Incremental steps of the specified algorithm are performed until the bars are sorted from shortest to tallest.


## Features
- Command line specification for the seven sorting algorithms
- Sliders to control data size and animation speed
- Colored bars to highlight key pieces of data being evaluated at each step

## Installation
1. Clone repository
```bash
> git clone https://github.com/wgreenwood4/portfolio.git
> cd sorting-visualizer
```
2. Install dependencies
```bash
> pip install -r requirements.txt
```
3. Run script
```bash
> python sorting-visualizer.py [algorithm]
```

## Usage
Upon running the script with no command line arguments, the following is the expected output:
```bash
> python sorting-visualizer.py
Select one sorting algorithm from:
  bubble      insertion   selection   shell     
  merge       quick       heap
```
If bubble sort is the desired sorting algorithm, the command line argument is used like so:
```bash
> python sorting-visualizer.py bubble
```
From here, the visualization tool will launch, and the user can:
* Click 'play' to begin the animation with current settings
* Change the size of the data and the animation speed with the sliders

***Note:*** Changing the sliders resets and effectively "pauses" the animation. The 'play' button will need to be clicked again upon moving the sliders.

To run a different sorting algorithm, simply close the tool and run the script again with a new command line argument.