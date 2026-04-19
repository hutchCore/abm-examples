# abm-examples
Common agent-based model examples developed in Mesa. These can be used for learning or as a place to start when developing other models. 

## Setup your Environment
1. Create and activate a virtual environment
2. Install Mesa: 
```bash 
pip install -U "mesa[rec]"
```
3. Install Jupyter Notebook (optional)
```bash
pip install jupyter
```
4. Install Seaborn (used for data visualization)
```bash
pip install seaborn
```

## Important Code Dependancies
```python
# Has multi-dimensional arrays and matrices.
# Has a large collection of mathematical functions to operate on these arrays.
import numpy as np

# Data manipulation and analysis.
import pandas as pd

# Data visualization tools.
import seaborn as sns

import mesa
```

## Run Things

Run Jupyter Notebook locally
```bash
jupyter lab
```


## References
- [Creating your First Model (with Mesa)](https://mesa.readthedocs.io/latest/tutorials/0_first_model.html)
- [Mesa GitHub Examples](https://github.com/mesa/mesa/tree/main/mesa/examples)
- [Mesa Model Code Best Practices](https://mesa.readthedocs.io/stable/best-practices.html)

