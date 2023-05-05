#this file is for importing the controller files to the app.py file

#__all__=["report_controller"]

#this above code cannot automatically identify new files in the controller, so another method is below

import os
import glob

__all__=[os.path.basename(f)[:-3] for f in glob.glob(os.path.dirname(__file__) + "/*.py")]