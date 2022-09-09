#!/bin/bash
PROJDIR=$(pwd)/..
CONFDIR=${PROJDIR}/dagfiles/dagconfs

run_dag1() {
	OLDDIR=$(pwd)
	cd ${PROJDIR}/sim
	case $1 in
		dr)
			python3 simulation.py ${CONFDIR}/dag1/dag1_dr_ws_config.json "dag1 delayrange"
		;;
		*)
			python3 simulation.py ${CONFDIR}/dag1/dag1_ws_config.json "dag1 default"
		;;
	esac
}
run_dag2() {
OLDDIR=$(pwd)
	cd ${PROJDIR}/sim

}

case $1 in
	1)
	;;
	2)
	;;
	*)
		echo "Invalid arg"
	;;
esac
