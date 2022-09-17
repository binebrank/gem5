#!/bin/bash

current_sim="/home/jusers/brank1/juawei/gem5_armhost"
DTIME=$(date '+%Y%m%d--%H-%M')

SRC_DIR="/home/jusers/brank1/juawei/STREAM"

SVE_SIZES=( 128 256 512 )
ITERS=3
OMPS=( 1 )
CASES=( 10000000 )
#OMPS=( 4 )
#CASES=( 40000000 )

for SVE in ${SVE_SIZES[@]}; do # loop over SVE sizes

BUILDS=( \
build-gem5-sve${SVE}-openmp \
)
GEM5_SVE=$(( $SVE / 128 ))

for OMP in ${OMPS[@]}; do # loop over OMP threads

for BUILD in ${BUILDS[@]}; do

BUILD_DIR="$SRC_DIR/$BUILD" # loop over different builds

for CASE in ${CASES[@]}; do # loop over workloads

OUTPUT="$CASE-$SVE-N1-${OMP}omp-neon-1channel"

BIN="${SRC_DIR}/stream_c_sve_gem5roi.exe"

OPTIONS="${CASE} ${ITERS}"

ulimit -s unlimited

${current_sim}/build/ARM/gem5.opt -d results-stream-sve-nopref/${OUTPUT}-${DTIME} -r  ${current_sim}/configs/example/se.py  --cpu-type=O3_ARM_Neoverse_N1 --num-cpus=4 --caches --l3_size=8MB --mem_latency=50ns --mem_bandwidth=25.6GB/s --mem-size=1GB --cpu-clock=2.5GHz --sys-clock=2.5GHz --param system.cpu[:].isa[:].sve_vl_se=${GEM5_SVE} --cmd="${BIN}" -o "${OPTIONS}" -e env${OMP}.sh --mem-type SimpleMemory --mem-channels=1 --mem-ranks=1 --disablehwp &

done # CASE

done # BUILD

done # OMPS

done # SVE

