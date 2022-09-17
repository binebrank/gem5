#!/bin/bash


current_sim="/home/jusers/brank1/juawei/gem5_armhost"
DTIME=$(date '+%Y%m%d--%H-%M')

SRC_DIR="/home/jusers/brank1/juawei/gromacs"

SVE_SIZES=( 128 256 512 )
#SVE_SIZES=( 128 )
ITERS=10
OMPS=( 1 )
#OMPS=( 2 )
CASES=( 4 )
#CASES=( 4 )

SIMD_KERNELS=("4xm" "4xm 2xmm" "2xmm")
#CASES=( water-0.96k water-1.5k water-3k water-6k water-12k water-24k )
#CASES=( water-0.96k )

cnt=0
for SVE in ${SVE_SIZES[@]}; do # loop over SVE sizes

BUILDS=( \
build-sve-${SVE}-gem5roi \
)

GEM5_SVE=$(( $SVE / 128 ))

for SIMD in ${SIMD_KERNELS[cnt]}; do # loop over SVE sizes

for OMP in ${OMPS[@]}; do # loop over OMP threads

for BUILD in ${BUILDS[@]}; do

BUILD_DIR="$SRC_DIR/$BUILD" # loop over different builds

for CASE in ${CASES[@]}; do # loop over workloads

OUTPUT="$CASE-N1-${OMP}omp-sve${SVE}-${SIMD}-${DTIME}"

BIN="${BUILD_DIR}/bin/gmx"

OPTIONS="nonbonded-benchmark -size ${CASE} -simd ${SIMD} -nt 1 -iter $ITERS -warmup 2 -time"

ulimit -s unlimited

${current_sim}/build/ARM/gem5.opt -d results-nonbonded-sameflop/${OUTPUT} -r  ${current_sim}/configs/example/se.py  --cpu-type=O3_ARM_Neoverse_N1_${SVE} --num-cpus=4 --caches --l3_size=8MB --mem_latency=50ns --mem_bandwidth=25.6GB/s --mem-size=1GB --cpu-clock=2.5GHz --sys-clock=2.5GHz --param system.cpu[:].isa[:].sve_vl_se=${GEM5_SVE} --cmd="${BIN}" -o "${OPTIONS}" --mem-type SimpleMemory --mem-channels=1 --mem-ranks=1 &

done # CASE

done # BUILD

done # OMPS

done # SIMD
let cnt=$cnt+1
done # SVE

