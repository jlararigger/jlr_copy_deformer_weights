
### jlr_copy_deformer_weights.py - Python Script
**Author: Juan Carlos Lara.**

**Description:**

Tool for copy the deformer weights from one deformer to other deformer.

**Install:**

1- Copy this script file to your scripts directory.

2- In the userSetup.py add the following lines:

    import maya.cmds as cmds
    import jlr_copy_deformer_weights
    
    cmds.evalDeferred('jlr_copy_deformer_weights.create_menu_commands()')
