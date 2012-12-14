#!/bin/bash
git clone http://apt-rpm.org/scm/apt.git || exit 1
mv apt $1-git$2
tar --remove-files -cJvf $1-git$2.tar.xz $1-git$2
