#!/bin/bash

current_sim="/home/jusers/brank1/juawei/gem5_armhost"
DTIME=$(date '+%Y%m%d--%H-%M')

SRC_DIR="/home/jusers/brank1/juawei/gromacs_proxy"

SVE_SIZES=( 128 256 512 1024 2048 )
ITERS=10
OMPS=( 1 )
CASES=( 1600 )
#CASES=( 100 )

for SVE in ${SVE_SIZES[@]}; do # loop over SVE sizes

BUILDS=( \
build-gem5-sve${SVE}-openmp \
)
GEM5_SVE=$(( $SVE / 128 ))

for OMP in ${OMPS[@]}; do # loop over OMP threads

for BUILD in ${BUILDS[@]}; do

BUILD_DIR="$SRC_DIR/$BUILD" # loop over different builds

for CASE in ${CASES[@]}; do # loop over workloads

OUTPUT="$CASE-N${ITERS}-${OMP}omp-${SVE}"

BIN="${SRC_DIR}/gromacs_gem5roi.x"

OPTIONS="${CASE} ${ITERS}"

ulimit -s unlimited

${current_sim}/build/ARM/gem5.opt -d results-gatherload1/${OUTPUT}-${DTIME} -r  ${current_sim}/configs/example/se.py  --cpu-type=O3_ARM_Neoverse_N1 --num-cpus=1 --caches --l3_size=8MB --mem_latency=50ns --mem_bandwidth=25.6GB/s --mem-size=1GB --cpu-clock=2.5GHz --sys-clock=2.5GHz  --param system.cpu[:].isa[:].sve_vl_se=${GEM5_SVE}  --cmd="${BIN}" -o "${OPTIONS}" --mem-type SimpleMemory --mem-channels=1 --mem-ranks=1 -e env${OMP}.sh &

done # CASE

done # BUILD

done # OMPS

done # SVE

