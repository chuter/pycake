# @Author: chuter
# @Date:   2021-08-08
# @Last Modified by:   chuter

#!/bin/sh

cd ..

pip3 install -U pipenv -i https://pypi.tuna.tsinghua.edu.cn/simple
pip3 install -U py.cake -i https://pypi.tuna.tsinghua.edu.cn/simple

py.cake release --docker

mv .release .tcloud/

cd .tcloud/
exit 0