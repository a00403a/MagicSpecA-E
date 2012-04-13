#!/bin/sh

/usr/lib/rpm/find-requires $* | egrep -v 'perl\(Automake' | sort -u | sed -e 's/\/bin\/perl/\/usr\/bin\/perl/g'
