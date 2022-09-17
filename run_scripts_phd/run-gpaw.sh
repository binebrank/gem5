#!/bin/bash


current_sim="/home/jusers/brank1/juawei/gem5_armhost"
DTIME=$(date '+%Y%m%d--%H-%M')

SRC_DIR="/home/jusers/brank1/juawei/gpaw-benchmarks"

SVE_SIZES=( 128 256 512 )
ITERS=10
OMPS=( 1 )
#OMPS=( 2 )
#CASES=( 1000 )

VECTORIZATION=( 1 2 3 )
CASES=( normal )
#CASES=( small )

BUILDS=( \
bmgs_fd \
construct_density \
)

for SVE in ${SVE_SIZES[@]}; do # loop over SVE sizes

GEM5_SVE=$(( $SVE / 128 ))

for CASE in ${CASES[@]}; do # loop over CASES

for BUILD in ${BUILDS[@]}; do # loop over build // unnecessary

BUILD_DIR="$SRC_DIR/$BUILD" # loop over different builds

for VEC in ${VECTORIZATION[@]}; do # loop over workloads

OUTPUT="vec${VEC}-${CASE}-${BUILD}-${SVE}"

BIN="${BUILD_DIR}/${CASE}_sve_gem5roi.exe"

OPTIONS="${VEC}"

ulimit -s unlimited

${current_sim}/build/ARM/gem5.opt -d results-gpawscalar-sameflops/${OUTPUT}-${DTIME} -r  ${current_sim}/configs/example/se.py  --cpu-type=O3_ARM_Neoverse_N1_${SVE} --num-cpus=1 --caches --l3_size=8MB --mem_latency=50ns --mem_bandwidth=25.6GB/s --mem-size=1GB --cpu-clock=2.5GHz --sys-clock=2.5GHz --param system.cpu[:].isa[:].sve_vl_se=${GEM5_SVE} --cmd="${BIN}" -o "${OPTIONS}" --mem-type SimpleMemory --mem-channels=1 --mem-ranks=1 &

done # VECTORIZATION

done # BUILD

done # CASES

done # SVE
