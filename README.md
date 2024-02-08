# Reconciling Conflicting Data Curation Actions: Transparency Through Argumentation

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/idaks/Games-and-Argumentation)


## Overview
This repository serve as the centralized place to document all scripts related to the work we published on [IDCC 2024](https://dcc.ac.uk/events/idcc24/programme)

>Xia, Y., Bowers, S., Li, L., & Ludäscher, B. (2024). Reconciling Conflicting Data Curation Actions: Transparency Through Argumentation. International Journal of Digital Curation, 18.

**Data Curation** with the dataset `citation.csv` and the two recipes `alice_recipe.json` and `bob_recipe.json`, you can easily replicate the process illustrated in the paper section 3.

**Resolve Argumentation Frame** By importing the `lib/gamearg.py`, with the translated logic programming facts, you can then run the script to resolve the AF and see the output.

## Codespace Setup

To set up your environment, simply click on the `Open in GitHub Codespaces` button above. Once the environment setup is complete, you'll be presented with an online version of VScode.

> **Notice:** If you encounter alerts like "Container build failed. Check troubleshooting guide" or "This codespace is currently running in recovery mode due to a configuration error", don't panic. Just press `Ctrl+Shift+P` and type `>Codespaces: Full Rebuild Container` to resolve the issue.

This process will take around 4-8 minutes. **Please do not** press any button until you see something like: `@username  ➜ /workspaces/Games-and-Argumentation (main) $ `

#### For Non-First-Time Usage
You can find the codespace you created at [this link](https://github.com/codespaces).

### Launch Jupyter

After setting up the codespace environment:

1. Type `jupyter lab` in the Terminal of the VScode online version.
   
   > **Notice:** Sometimes, due to codespace limitations, the terminal may go blank. Simply refreshing your browser should solve the problem.

2. This will lead you to the Jupyter Lab interface, where you can run:
   - `Tutorial.ipynb`

---


## Local Setup
```
conda env create -f environment.yaml
conda activate gamearg
```

## Contact

For any queries related to the code:
- Open an issue on GitHub
- Contact: Yilin Xia ([yilinx2@illinois.edu](mailto:yilinx2@illinois.edu))

