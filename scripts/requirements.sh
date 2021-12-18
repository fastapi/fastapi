#!/bin/bash

pip3 install -r requirements.txt || exit 1

case "$OSTYPE" in
  solaris* | darwin* | linux* | bsd*) flit install --deps develop --symlink ;;
  msys* | cygwin*) flit install --deps develop --pth-file ;;
  *)  echo "unknown: $OSTYPE, please follow CONTRIBUTION.MD instructions manually." ;;
esac
