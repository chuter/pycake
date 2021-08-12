# @Author: chuter
# @Date:   2021-08-08
# @Last Modified by:   chuter

#!/bin/sh

cd ..

pip3 install -U py.cake

py.cake release --docker

mv .release .tcloud/

cd .tcloud/.release