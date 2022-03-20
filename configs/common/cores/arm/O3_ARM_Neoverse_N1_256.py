from m5.objects import *
from common.cores.arm.O3_ARM_v7a import *
from common.cores.arm.O3_ARM_Neoverse_N1 import *
from common.Caches import *

# Sources for this configuration:
# (1) https://en.wikichip.org/wiki/arm_holdings/microarchitectures/neoverse_n1
# (2) https://developer.arm.com/documentation/swog309707/latest
# (3) The Arm Neoverse N1 Platform: Building Blocks for the Next-Gen Cloud-to-Edge Infrastructure SoC, white paper
# (4) https://chipsandcheese.com/2021/10/22/deep-diving-neoverse-n1/
# (5) https://github.com/aakahlow/gem5Valid_Haswell

# Latencies of L1 L2 and L3 cache were taken from (5) but modified to match those in (3)
# Also refer to https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9059267&tag=1
# why Icache has latencies 1
# Haswell latencies: L1 = 4 cyles, L2 = 12 cycles, L3 = 36 cycles
# Neo-n1  latencies: L1 = 4 cyles, L2 = 11 cycles, L3 = 28-33 cycles

class O3_ARM_Neoverse_N1_FP_256(FUDesc):
    oplist = [ opdesc(opclass='simdadd', oplat=2), # asimd arithmetic basis (add & sub)
               opdesc(opclass='simdaddacc', oplat=4), # asimd absolute diff accum (vaba)
               opdesc(opclass='simdalu', oplat=2), # asimd logical (and)
               opdesc(opclass='simdcmp', oplat=2), # asimd compare (cmeq)
               opdesc(opclass='simdcvt', oplat=3), # asimd fp convert to floating point 64b (scvtf)
               opdesc(opclass='simdmisc', oplat=2), # asimd move, immed (vmov)
               opdesc(opclass='simdmult',oplat=4), # asimd integer multiply d-form (mul)
               opdesc(opclass='simdmultacc',oplat=4), # asimd multiply accumulate, d-form (mla)
               opdesc(opclass='simdshift',oplat=2), # asimd shift by immed, (shl)
               opdesc(opclass='simdshiftacc', oplat=4), # asimd shift accumulate (vsra)
               opdesc(opclass='simdsqrt', oplat=9), # asimd reciprocal estimate (vrsqrte)
               opdesc(opclass='simdfloatadd',oplat=2), # asimd floating point arithmetic (vadd)
               opdesc(opclass='simdfloatalu',oplat=2), # asimd floating point absolute value (vabs)
               opdesc(opclass='simdfloatcmp', oplat=2), # asimd floating point comapre (fcmgt)
               opdesc(opclass='simdfloatcvt', oplat=3), # aarch64 fp convert (fvctas)
               opdesc(opclass='simdfloatdiv', oplat=11, pipelined=false), # asimd floating point divide f64 (fdiv) // we take average latency
               opdesc(opclass='simdfloatmisc', oplat=2), # bunch of relatively non-important insts (vneg)
               opdesc(opclass='simdfloatmult', oplat=4), # asimd floating point multiply (vmul)
               opdesc(opclass='simdfloatmultacc',oplat=4), # asimd floating point multiply accumulate (vmla)
               opdesc(opclass='simdfloatsqrt', oplat=12, pipelined=false), # asimd floating point square root f64 (vsqrt) // we take average latency
               opdesc(opclass='simdreduceadd', oplat=4), # sve reduction, arithmetic, s form (saddv) 
               opdesc(opclass='simdreducealu', oplat=5), # sve reduction, logical (andv)
               opdesc(opclass='simdreducecmp', oplat=5), # sve reduction, arithmetic, s form (smaxv)
               opdesc(opclass='simdfloatreduceadd', oplat=4, pipelined=false), # sve floating point associative add (fadda) // same class for faddv, bad gem5 implementation
               opdesc(opclass='simdfloatreducecmp', oplat=5), # sve floating point reduction f64 (fmaxv)
               opdesc(opclass='floatadd', oplat=2), # aarch64 fp arithmetic (fadd)
               opdesc(opclass='floatcmp', oplat=2), # aarch64 fp compare (fccmpe)
               opdesc(opclass='floatcvt', oplat=3), # aarch64 fp convert (vcvt)
               opdesc(opclass='floatdiv', oplat=11, pipelined=false), # aarch64 fp divide (vdiv) // average latency
               opdesc(opclass='floatsqrt', oplat=12, pipelined=false), # aarch64 fp square root d-form (fsqrt) // average latency
               opdesc(opclass='floatmultacc', oplat=4), # aarch64 fp multiply accumulate (vfma)
               opdesc(opclass='floatmisc', oplat=3), # aarch64 miscelleaneaus
               opdesc(opclass='floatmult', oplat=3) ] # aarch64 fp multiply (fmul)

    count = 2 

class O3_ARM_Neoverse_N1_FUP_256(FUPool):
    FUList = [O3_ARM_Neoverse_N1_Simple_Int(),
              O3_ARM_Neoverse_N1_Complex_Int(),
              O3_ARM_Neoverse_N1_LoadStore(),
              O3_ARM_Neoverse_N1_FP_256()]

class O3_ARM_Neoverse_N1_256(O3_ARM_Neoverse_N1):
    fuPool = O3_ARM_Neoverse_N1_FUP_256()

