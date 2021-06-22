#!/bin/bash

conda activate csci_research
cd ~/eye_tracking_visualizer/docs
cd source
mv index.rst index.rst.keep
rm *.rst
mv index.rst.keep index.rst
cd ..
sphinx-apidoc -o ./source ../src
make clean
make html
