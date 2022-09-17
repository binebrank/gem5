#!/bin/bash

current_sim="/home/jusers/brank1/juawei/gem5_armhost"
DTIME=$(date '+%Y%m%d--%H-%M')

SRC_DIR="/home/jusers/brank1/juawei/NPB3.0-omp-C"
SVE_SIZES=( 128 )
ITERS=10
OMPS=( 1 )
CASES=( bt.S cg.S ep.S ft.S is.S lu.S mg.S sp.S )
CASES=( is.S is.W )
#CASES=( bt.W cg.W ep.W ft.W is.W lu.W mg.W sp.W )
#CASES=( bt.S cg.S ep.S ft.S is.S lu.S mg.S sp.S bt.W cg.W ep.W ft.W is.W lu.W mg.W sp.W )

for SVE in ${SVE_SIZES[@]}; do

GEM5_SVE=$(( $SVE / 128 ))

BUILD_DIR="$SRC_DIR"

for CASE in ${CASES[@]}; do

for OMP in ${OMPS[@]}; do # loop over OMP threads

OUTPUT="$CASE-${OMP}omp-N1"

BIN="${BUILD_DIR}/bin/${CASE}"

OPTIONS=" "

ulimit -s unlimited

${current_sim}/build/ARM/gem5.opt -d results-npb/${OUTPUT}-${DTIME} -r  ${current_sim}/configs/example/se.py  --cpu-type=O3_ARM_Neoverse_N1 --num-cpus=4 --caches --l3_size=8MB --mem_latency=50ns --mem_bandwidth=25.6GB/s --mem-size=1GB --cpu-clock=2.5GHz --sys-clock=2.5GHz  --param system.cpu[:].isa[:].sve_vl_se=${GEM5_SVE}  --cmd=${BIN} -o "${OPTIONS}" -e env${OMP}.sh --mem-type SimpleMemory --mem-channels=1 --mem-ranks=1 &

done # OMP

done # CASE

done # SVE

