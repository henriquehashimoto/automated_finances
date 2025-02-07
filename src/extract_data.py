import pandas as pd
from dotenv import load_dotenv
import os
import gdown

#==================================================
#   Getting folder parameter from .venv file (this file is gitignore read Notion to get what's inside of it)
#==================================================
load_dotenv()
folder = os.getenv('url_folder')

gdown.download_folder(folder, output="data",quiet=False,use_cookies=False)


