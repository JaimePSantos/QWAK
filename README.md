# QWAK
Quantum Walk Analysis Kit - Continuous-time quantum walk analysis framework.



## Table of Contents:

-  [Installation](#installation)
-  [Usage](#usage)
-  [Documentation](#documentation)
-  [Contributing](#contributing)

## Requirements
- Numpy
- Scipy
- Sympy
- matplotlib
- networkx
- QuTip
- eel

## Installation

Installing the package is very straightforward. Firstly, clone the project and then install the requirements via pip, followed by `pip install .` in the cloned folder. A virtual environment is highly recommended.

Step-by-step installation instructions can be found in the documentation [installation](https://jaimepsantos.github.io/QWAK/installation.html) page.



## Usage
A basic plot of the probability distribution for a CTQW with a walker starting in a superposition of central positions, in a cyclic graph, can be achieved via the following example:
```python
import networkx as nx
import matplotlib.pyplot as plt
from qwak.qwak import QWAK

n = 100
t = 12
initState = [n//2,n//2 + 1]
graph = nx.cycle_graph(n)

qwak = QWAK(graph)
qwak.runWalk(t,initState)

probVec = qwak.getProbVec()
plt.plot(probVec)
plt.show()
```
Further examples exploring all the different components will be available once the [usage](https://jaimepsantos.github.io/QWAK/usage.html) documentation is complete.

## Documentation
Documentation is a work in progress, and can be found in this [page](https://jaimepsantos.github.io/QWAK/).

## Contributing
#### Changes to the package
1. Upgrade your build package with `python -m pip install --upgrade build`.
2. Edit the package to reflect your changes.
3. Build the distribution files by running `python -m build`.
4. Reinstall the package without using previously cached versions with `pip install . --no-cache-dir`.
5. For some reason in windows you may need to use `python -m pip install . --no-cache-dir --use-feature=in-tree-build`

#### Commit the changes the github repo
1. Fork the repository
2. Clone your github fork git ```clone https://github.com/<your-username>/QWAK.git```
3. Navigate to the project folder ```cd QWAK```
4. Add the upstream repo ```git remote add upstream https://github.com/JaimePSantos/QWAK.git```
5. Update your fork with ```git checkout main``` and ```git pull --rebase upstream main```
6. Create a branch for the changes instead of working off your local main branch ```git checkout -b <new branch name> upstream/main```
7. Make your changes.
8. Format your code with ```autopep8 --in-place --aggressive --aggressive --max-line-length 72 .\core\qwak\qwak.py```
9. Commit your changes: ```git commit -am <Commit message>```
10. Push your changes to your fork ```git push -u origin <branch name>```
11. Visit your repo on github and create a pull request to the main repo!

#### Building Documentation
1. Install the [sphinx](https://www.sphinx-doc.org/en/master/) `pip install sphinx`
2. Generate basic documentation files for the package `sphinx-quickstart documentation/` (probably already present in the repo so just skip)
3. Generate autodoc files from the modules you want to document `sphinx-apidoc -f -o source/ ../core/<modules>`
4. Clean previous build files `make clean`
5. Build html documentation page `make html`
6. Copy the new contents to docs folder for github pages `make linuxgit` or `make github`
