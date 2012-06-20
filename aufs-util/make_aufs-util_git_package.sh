#!/bin/bash
git clone git://aufs.git.sourceforge.net/gitroot/aufs/aufs-util.git \
	aufs-util.git || exit 1
pushd aufs-util.git
git checkout origin/aufs3.0
popd
pushd aufs-util.git
find . -name .git|xargs rm -rf
popd
mv aufs-util.git $1-git$2
tar --remove-files -cJvf $1-git$2.tar.xz $1-git$2


