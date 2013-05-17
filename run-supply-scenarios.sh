#!/bin/sh
#
# Run all of the scenarios for the final journal paper.

PYTHON=python26
EVOLVE=~/code/evolve.py
EVOPTS="-g 10"

# Sensitivity to coal CCS capital costs
for ccscost in `seq 4000 500 6000`; do
    for storcost in 20 40 60 80 100 ; do
	for lowhigh in --low-cost --high-cost ; do
            $PYTHON $EVOLVE $EVOPTS -s coal-ccs $lowhigh --coal-ccs-costs=$ccscost \
		--ccs-storage-costs=$storcost
	done
    done
done

# Sensitivity to CCS transport costs
for scenario in coal-ccs ccgt-ccs ; do
    for ccs in 20 40 60 80 100 ; do
        for co2price in 23 50 70 90 125 ; do
            $PYTHON $EVOLVE $EVOPTS -s $scenario --ccs-storage-costs=$ccs -c $co2price
        done
    done
done

# Sensitivity to gas price and CO2 price
for scenario in ccgt ccgt-ccs coal-ccs replacement ; do
    for gasprice in 6 9 12 15 ; do
	for co2price in 0 23 50 70 90 125 ; do
	    $PYTHON $EVOLVE $EVOPTS -s $scenario --gas-price=$gasprice -c $co2price
        done
    done
done