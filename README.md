# AP-Lines

Contributors:
Selina Breitenbach, Timo Ege, Jan Müller

This python module was created as the results of a beginner programming practical

## Usage

This module can be used like other python modules, after the location is addded to the python system path,

``` python
import sys
sys.path.append("path to lines folder, not including lines")
```

if you only want to play the game, in the folder containing the 'lines' foulder execute the following command:

``` cmd
python -m lines.visulatization.mainWindow
```

## Package structure

the module is structured into three parts.
'Base' containing the graph implementation in 'graph.py'; additional functions to be used on graphs in 'graph_functions.py'. 

The second is 'optimization' containing implementations of the dijkstra algorithm and the floydWarshall algorithm as well as the following functions: best_start_point; best_start_node_index; construct_path; 

The third part being 'visualization' containing the functions to play the game

