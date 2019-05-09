export LANG=en_US.UTF-8

conda build openalea.deploy
conda install --use-local openalea.deploy

conda build ann
conda install --use-local ann

conda build cgal
conda install --use-local cgal

conda build libqglviewer
conda install --use-local libqglviewer

conda build pyqglviewer
conda install --use-local pyqglviewer

conda build qhull
conda install --use-local qhull

conda build plantgl
conda install --use-local plantgl

conda build lpy
conda install --use-local lpy

conda build mtg
conda install --use-local mtg

conda build plantscan3d
conda install --use-local plantscan3d
