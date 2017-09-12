#!/bin/sh

echo '$ venv/bin/python segment.py'
venv/bin/python segment.py
echo '--'

echo '$ venv/bin/python preprocess.py'
venv/bin/python preprocess.py
echo '--'

echo '$ venv/bin/python extract.py'
venv/bin/python extract.py
echo '--'

echo '$ venv/bin/python split.py'
venv/bin/python split.py
echo '--'

echo 'All done!'