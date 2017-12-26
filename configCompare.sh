#!/bin/sh
#================================================================
#  [Wey Gu] Openstack Configuration Compare
#      A Tool to compare two nodes conf, enabled by Openstack Oslo_config.
#      https://github.com/littlewey/openstack_Conf_Compare
#  EXAMPLES
#      configCompare.sh <path of Folder A> <path of Folder B>
#
#================================================================
#  HISTORY
#      2017/12/26 : Wey Gu: initial creation
#
#================================================================

VERSION=0.1
USAGE="Usage: command -hv args"
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color
#================================================================
# END_OF_HEADER
#================================================================

if [ -z "$2"  ] ; then
    echo "[${RED}ERR${NC}] No Folder Path Providedi ! Follow below format Please :-)"
    echo "+=============================================================+"
    echo "|Usage: configCompare.sh <path of Folder A> <path of Folder B>|"
    echo "+=============================================================+"
else
    echo "[${GREEN}OK${NC}] configCompare started ..."
    env/bin/python compareConfFolder.py $1 $2
fi
