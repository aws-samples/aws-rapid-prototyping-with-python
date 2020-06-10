#!/bin/bash
PYTHON_VERSION=3.7
LIB_DIR=python/lib/python$PYTHON_VERSION/site-packages
INSTALLER=pip$PYTHON_VERSION

[ -e $LIB_DIR ] && rm -r $LIB_DIR
[ -e pandas.zip ] && rm pandas.zip

which $INSTALLER >& /dev/null
[ $? -ne 0 ] && INSTALLER=pip3
echo "pip => $INSTALLER"

mkdir -p $LIB_DIR
$INSTALLER install pandas xlrd xlwt xlsxwriter -t $LIB_DIR
zip pandas.zip python/ -r
aws lambda publish-layer-version --layer-name pandas --zip-file fileb://./pandas.zip --compatible-runtimes python$PYTHON_VERSION --region ap-northeast-1
