import os.path

from 工具.common import traverse_folder, remove_bg, convert_to1

_,files = traverse_folder('.',True)
for file in files:
    if not file.endswith('.png') or '_no_bg'  in file or '_to1' in file:
        continue
    # name =file.replace( os.path.basename(file),f'{os.path.basename(file)}_no_bg.png')
    # remove_bg(file,name)

    name = file.replace(os.path.basename(file), f'{os.path.basename(file)}_to1.png')
    convert_to1(file,name)