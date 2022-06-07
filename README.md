# QWAK
Quantum Walk Analysis Kit - Continuous-time quantum walk analysis framework.

[Documentation](https://jaimepsantos.github.io/QWAK/ ).

## Requirements
- Numpy
- Scipy
- Sympy
- matplotlib
- networkx
- eel

## Installation Instructions
#### Cloning the repository
1. Clone the [repository](https://github.com/qwchagas/qwak): `git clone <link to repo>`
2. Navigate to the cloned directory

#### Setup Virtual environment (optional but recommended)
##### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Using python venv
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 3. Once inside the cloned repo, create a python virtual environment: `python3 -m venv qwakEnv`

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 4. Create a shortcut for the activation executable: `ln -s /qwakEnv/bin/activate qwakEnv`

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 5. Activate the environment: `source qwakEnv`

#####  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Using conda
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 3. Alternatively, create a conda environment inside the cloned repo with `conda create -n qwakEnv`

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 4/5. Activate the conda environment with `conda activate qwakEnv`


#### Installing the package
6. Install required python dependencies: `pip install numpy scipy sympy matplotlib networkx`
7. Install [eel](https://github.com/ChrisKnott/Eel) if you want to use the GUI: `pip install eel`
8. Install the qwak package: `pip install .`

#### Testing the installation
9. Run the basic testing suite: `python installCheck.py`

#### Running the GUI
10. From the `qwak` folder, navigate to the `core` folder using `cd core`.
11. Run the GUI file with the command `python gui-main.py`.

## Using the package
(Under construction)

## Contributing to the package
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
8. Commit your changes: ```git commit -am <Commit message>```
9. Push your changes to your fork ```git push -u origin <branch name>```
10. Visit your repo on github and create a pull request to the main repo!

#### Building Documentation
1. Install the [sphinx](https://www.sphinx-doc.org/en/master/) `pip install sphinx`
2. Generate basic documentation files for the package `sphinx-quickstart documentation/` (probably already present in the repo so just skip)
3. Generate autodoc files from the modules you want to document `sphinx-apidoc -f -o source/ ../core/<modules>`
4. Clean previous build files `make clean`
5. Build html documentation page `make html`
6. Copy the new contents to docs folder for github pages `make linuxgit` or `make github`
