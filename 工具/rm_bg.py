import os.path

from 工具.convert_to_1 import convert
from 工具.convert_to_l import convert_l
from 工具.remove_bg import remove_bg
for i in range(4):
    name=f"parts_{i+1}.png"
    # print(os.path.isfile(name))
    # new=f"parts_{i+1}_to1.png"
    # # convert(name,new)
    #
    new2=f"parts_{i+1}_nobg.png"
    # remove_bg(name,new2)
    #
    # convert(new2,new)

    l_name = f"parts_{i+1}_toLLLL1.png"
    convert_l(new2,l_name)

