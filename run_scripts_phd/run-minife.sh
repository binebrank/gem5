#!/bin/bash


current_sim="/home/jusers/brank1/juawei/gem5_armhost"
DTIME=$(date '+%Y%m%d--%H-%M')

SRC_DIR="/home/jusers/brank1/juawei/minife/src/miniFE_sve/openmp-sve/src"

SVE_SIZES=( 128 256 512 )
#SVE_SIZES=( 128 )
ITERS=10
OMPS=( 1 4 )
#OMPS=( 2 )
#CASES=( 1000 )

CASES=( 50 55 60 )
#CASES=( 10 )
FORMAT=( csrfast csr sell )

for SVE in ${SVE_SIZES[@]}; do # loop over SVE sizes

for FORM in ${FORMAT[@]}; do # loop over SVE sizes

BUILDS=( \
build_${FORM}_sve_gem5roi \
)

GEM5_SVE=$(( $SVE / 128 ))

for OMP in ${OMPS[@]}; do # loop over OMP threads

for BUILD in ${BUILDS[@]}; do

BUILD_DIR="$SRC_DIR/$BUILD" # loop over different builds

for CASE in ${CASES[@]}; do # loop over workloads

OUTPUT="${OMP}omps-$CASE-N1-${BUILD}-${SVE}"

BIN="${BUILD_DIR}/miniFE.x"

OPTIONS=" -nx ${CASE} -ny ${CASE} -nz ${CASE} -output_dir results-minife/${OUTPUT}-${DTIME}"
#OPTIONS=" "

ulimit -s unlimited

${current_sim}/build/ARM/gem5.opt -d results-minife_singleroi/${OUTPUT}-${DTIME} -r  ${current_sim}/configs/example/se.py  --cpu-type=O3_ARM_Neoverse_N1_${SVE} --num-cpus=${OMP} --caches --l3_size=8MB --mem_latency=50ns --mem_bandwidth=25.6GB/s --mem-size=1GB --cpu-clock=2.5GHz --sys-clock=2.5GHz --param system.cpu[:].isa[:].sve_vl_se=${GEM5_SVE} --cmd="${BIN}" -o "${OPTIONS}" --mem-type SimpleMemory --mem-channels=1 --mem-ranks=1 &

done # CASE

done # BUILD

done # OMPS

done # FORM

done # SVE

