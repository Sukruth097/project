import os
from pathlib import Path

package_name = 'src'

list_of_files = [ 
    f"{package_name}/__init__.py",
    f"{package_name}/config/__init__.py",
    f"{package_name}/cloud/__init__.py",
    f"{package_name}/entity/__init__.py",
    f"{package_name}/entity/config_entity.py",
    f"{package_name}/entity/artifact_entity.py",
    f"{package_name}/entity/metadata_entity.py",
    f"{package_name}/exception/__init__.py",
    f"{package_name}/logger/__init__.py",
    f"{package_name}/utils/__init__.py",
    f"{package_name}/components/__init__.py",
    f"{package_name}/components/training/dataingestion.py",
    f"{package_name}/pipeline/__init__.py",
    "requirements.txt",
    "app.py"
]

for file_path in list_of_files:
    file_path = Path(file_path)
    file_dir , file_name = os.path.split(file_path)
    
    if file_dir!= '':
        os.makedirs(file_dir, exist_ok=True)

    if (not os.path.exists(file_path)) or (os.path.getsize(file_path)==0):
        with open(file_path,"w") as f:
            pass # Create an empty file and do nothing