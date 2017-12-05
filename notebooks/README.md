# SynapseAnalysis
## Jupyter Notebooks

Index: (to be populated)
- 
- 
- 

If "module not found" error, add the following snippit: 

```
import os
import sys
module_path = os.path.abspath(os.path.join('..'))
module_path = module_path + '/code/'
if module_path not in sys.path:
    sys.path.append(module_path)
```