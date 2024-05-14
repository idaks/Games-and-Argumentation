# On the Structure of Game Provenance and its Applications

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/idaks/Games-and-Argumentation/tree/tapp)


## Overview
This repository serves as the centralized place to document all scripts related to the work we published on [TaPP 2024](https://provenanceweek.github.io/TaPP2024/TaPP_2024.html) and you are more than welcome to check our paper.

## Codespace Setup

To set up your environment, simply click on the `Open in GitHub Codespaces` button above. Once the environment setup is complete, you'll be presented with an online version of VScode.

> **Notice:** If you encounter alerts like "Container build failed. Check troubleshooting guide" or "This codespace is currently running in recovery mode due to a configuration error", don't panic. Just press `Ctrl+Shift+P` and type `>Codespaces: Full Rebuild Container` to resolve the issue.

This process will take around 4-8 minutes. **Please do not** press any button until you see something like: `@username  ➜ /workspaces/Games-and-Argumentation (tapp) $ `

#### For Non-First-Time Usage
You can find the codespace you created at [this link](https://github.com/codespaces).


## Local Setup
```
conda env create -f environment.yaml
conda activate gamearg
```

## Launch Jupyter

After setting up the codespace or your local conda environment:

1. Type `jupyter lab` in the Terminal.
   
   > **Notice:** Sometimes, due to codespace limitations, the terminal may go blank. Simply refreshing your browser should solve the problem.

2. This will lead you to the Jupyter Lab interface, where you can run:
   - `demo.ipynb`


## Contact

For any queries related to the code:
- Open an issue on GitHub
- Contact: Yilin Xia ([yilinx2@illinois.edu](mailto:yilinx2@illinois.edu))

