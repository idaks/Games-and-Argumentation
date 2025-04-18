# How to Use the Repository

## In Terminal

1. Clone the repository:
    ```bash
    git clone https://github.com/idaks/Games-and-Argumentation
    ```

2. Navigate to the cloned folder:
    ```bash
    cd Games-and-Argumentation
    ```

3. Create the Conda environment:
    ```bash
    conda env create -f environment.yaml
    ```

4. Activate the environment:
    ```bash
    conda activate gamearg
    ```

5. Open Jupyter Lab:
    ```bash
    jupyter lab
    ```

## In Jupyter

1. Navigate to the `refactor` folder (the current one).

2. You will see two notebooks: `arg.ipynb` and `game.ipynb`.

3. Change the input file (all input `.lp` files can be found under the `files` folder) to visualize different graphs.


**Note:** All input graphs should be in the WM graph format, meaning the predicate should only contain `move`.
