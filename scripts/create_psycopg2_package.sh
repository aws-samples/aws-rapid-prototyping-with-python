#!/bin/bash
PYTHON_VERSION=3.7
POSTGRES_VERSION=10.0
PSYCOPG2_VERSION=2.8.4

LIB_DIR=python/lib/python$PYTHON_VERSION/site-packages

POSTGRES_PATH=postgresql-$POSTGRES_VERSION
POSTGRES_URL=https://ftp.postgresql.org/pub/source/v$POSTGRES_VERSION/$POSTGRES_PATH.tar.gz
POSTGRES_INSTALL_PATH=/tmp/pg

PSYCOPG2_PATH=psycopg2-$PSYCOPG2_VERSION
PSYCOPG2_URL=https://files.pythonhosted.org/packages/84/d7/6a93c99b5ba4d4d22daa3928b983cec66df4536ca50b22ce5dcac65e4e71/$PSYCOPG2_PATH.tar.gz

function download_postgres {
    if [ -e $POSTGRES_PATH.tar.gz ]; then
        echo "skip download postgresql."
    else
        sudo yum install -y postgresql-devel
        wget $POSTGRES_URL
        tar -zxvf $POSTGRES_PATH.tar.gz
    fi
}

function install_postgres {
    if [ -e $POSTGRES_INSTALL_PATH ]; then
        echo "skip install postgresql."
    else
        cd $POSTGRES_PATH
        ./configure --prefix $POSTGRES_INSTALL_PATH --without-readline --without-zlib
        make
        make install
        cd ..
    fi
}

function install_psycopg2 {
    if [ -e $PSYCOPG2_PATH.tar.gz ]; then
        echo "skip download psycopg2."
    else 
        wget $PSYCOPG2_URL
        tar -zxvf $PSYCOPG2_PATH.tar.gz
    fi
    
    cd $PSYCOPG2_PATH
    sed -i -e "s#pg_config =.*#pg_config = $POSTGRES_INSTALL_PATH/bin/pg_config#" setup.cfg
    sed -i -e "s/static_libpq = 0/static_libpq = 1/" setup.cfg 
    LD_LIBRARY_PATH=$PG_DIR/lib:$LD_LIBRARY_PATH python$PYTHON_VERSION setup.py build
    cd ..
}

[ -e $LIB_DIR ] && rm -r $LIB_DIR
[ -e psycopg2.zip ] && rm -r psycopg2.zip

set -e
download_postgres
install_postgres
install_psycopg2

mkdir -p $LIB_DIR
cp -r  $PSYCOPG2_PATH/build/lib.linux-x86_64-$PYTHON_VERSION/psycopg2/ $LIB_DIR
zip psycopg2.zip python/ -r
aws lambda publish-layer-version --layer-name psycopg2 --zip-file fileb://./psycopg2.zip --compatible-runtimes python$PYTHON_VERSION --region ap-northeast-1
set +e

rm $POSTGRES_PATH.tar.gz $PSYCOPG2_PATH.tar.gz
rm -r $POSTGRES_PATH $PSYCOPG2_PATH $POSTGRES_INSTALL_PATH
echo 'done!'
