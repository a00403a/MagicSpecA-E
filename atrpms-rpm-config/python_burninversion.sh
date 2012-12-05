#! /bin/sh

which python > /dev/null 2>&1 || exit 0
python_version=`python -c "import sys; print sys.version[:3]"`

find ${RPM_BUILD_ROOT} -type f \
  | xargs grep -l '^#!.*python' \
  | xargs perl -pi -e's,^(#!.*python)[0-9.]*,${1}'$python_version,
