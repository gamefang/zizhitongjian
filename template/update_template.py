# -*- coding: utf-8 -*-
# python3.7+
# 处理csvtotable的模板(一次性)
# csvtotable安装完无法使用的话，需添加环境变量，大概位于：C:\Users\XXX\AppData\Roaming\Python\Python37\Scripts

import os
import shutil

try:
    import csvtotable
except Exception as e:
    print('Please first run cmd:\npip install csvtotable')
else:
    if not os.path.exists('__template.j2'):
        TPL_FP = os.path.join(csvtotable.__path__[0],'templates/template.j2')
        shutil.copy(TPL_FP,'__template.j2')
        shutil.copy('template.j2',TPL_FP)
        input(f'Already updated template in csvtotable!\n  Original path: {TPL_FP}\n  Backup file: __template.j2')