import os.path

from 工具.common import traverse_folder, remove_bg

_,files = traverse_folder('.',True)
for file in files:
    if not file.endswith('.png') or '_no_bg'  in file:
        continue
    name =file.replace( os.path.basename(file),f'{os.path.basename(file)}_no_bg.png')
    remove_bg(file,name)