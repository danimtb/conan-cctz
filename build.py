#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bincrafters import build_shared
from bincrafters import build_template_default

if __name__ == "__main__":

    builder = build_template_default.get_builder(pure_c=False)
    
    for b in builder.items:
        print(b.settings['compiler.libcxx'])
        
    if build_shared.get_os() == "Linux":
        builder.items = filter(lambda b: b.settings['compiler.libcxx'] == 'libstdc++11', builder.items)
    builder.run()
