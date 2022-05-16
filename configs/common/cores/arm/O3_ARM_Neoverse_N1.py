from m5.objects import *
from common.cores.arm.O3_ARM_v7a import *
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
class O3_ARM_Neoverse_N1_ICache(Cache):
    tag_latency = 1
    data_latency = 1
    response_latency = 1
    mshrs = 8
    tgts_per_mshr = 16
    size = '64kB' # (1)
    assoc = 4 # (1)
    writeback_clean = False
    prefetcher = StridePrefetcher(degree=1)

class O3_ARM_Neoverse_N1_DCache(Cache):
    tag_latency = 3
    data_latency = 3
    response_latency = 1
    tgts_per_mshr = 16
    writeback_clean = False
    size = '64kB' # (1)
    mshrs = 20 # (1)
    assoc = 4 # (1)
    #prefetcher = StridePrefetcher(degree=16, latency = 1)

class O3_ARM_Neoverse_N1_L2(Cache):
    tag_latency = 5
    data_latency = 5
    response_latency = 2 
    mshrs = 46  # (1)
    tgts_per_mshr = 16
    clusivity = 'mostly_incl' # (1)
    assoc = 8 # (1)
    size = '1MB' # Graviton2
    writeback_clean= True
    # do this in cache config prefetcher = TaggedPrefetcher(degree=16, latency = 1, queue_size = 16)

class O3_ARM_Neoverse_N1_L3(L3Cache):
    tag_latency = 48 
    data_latency = 48
    response_latency = 16 
    assoc = 16 # (1)
    size = '8MB' # 1MB per core-duplex but we set this higher due to shared L3 and interconnect
    # do this in cache config prefetcher = TaggedPrefetcher(degree=16, latency = 1, queue_size = 16)
    clusivity = 'mostly_excl'
    mshrs = 128

# This class refers to FP/ASIMD 0/1 (symbol V in (2) table 3)
class O3_ARM_Neoverse_N1_FP(FUDesc):
    # copied from Neoverse V1 optimization guide, latency taken for specific instruction in brackets
    opList = [ OpDesc(opClass='SimdAdd', opLat=2), # ASIMD arithmetic basis (add & sub)
               OpDesc(opClass='SimdAddAcc', opLat=4), # ASIMD absolute diff accum (vaba)
               OpDesc(opClass='SimdAlu', opLat=2), # ASIMD logical (and)
               OpDesc(opClass='SimdCmp', opLat=2), # ASIMD compare (cmeq)
               OpDesc(opClass='SimdCvt', opLat=3), # ASIMD FP convert to floating point 64b (scvtf)
               OpDesc(opClass='SimdMisc', opLat=2), # ASIMD move, immed (vmov)
               OpDesc(opClass='SimdMult',opLat=4), # ASIMD integer multiply D-form (mul)
               OpDesc(opClass='SimdMultAcc',opLat=4), # ASIMD multiply accumulate, D-form (mla)
               OpDesc(opClass='SimdShift',opLat=2), # ASIMD shift by immed, (shl)
               OpDesc(opClass='SimdShiftAcc', opLat=4), # ASIMD shift accumulate (vsra)
               OpDesc(opClass='SimdSqrt', opLat=9), # ASIMD reciprocal estimate (vrsqrte)
               OpDesc(opClass='SimdFloatAdd',opLat=2), # ASIMD floating point arithmetic (vadd)
               OpDesc(opClass='SimdFloatAlu',opLat=2), # ASIMD floating point absolute value (vabs)
               OpDesc(opClass='SimdFloatCmp', opLat=2), # ASIMD floating point comapre (fcmgt)
               OpDesc(opClass='SimdFloatCvt', opLat=3), # Aarch64 FP convert (fvctas)
               OpDesc(opClass='SimdFloatDiv', opLat=11, pipelined=False), # ASIMD floating point divide f64 (fdiv) // we take average latency
               OpDesc(opClass='SimdFloatMisc', opLat=2), # Bunch of relatively non-important insts (vneg)
               OpDesc(opClass='SimdFloatMult', opLat=4), # ASIMD floating point multiply (vmul)
               OpDesc(opClass='SimdFloatMultAcc',opLat=4), # ASIMD floating point multiply accumulate (vmla)
               OpDesc(opClass='SimdFloatSqrt', opLat=12, pipelined=False), # ASIMD floating point square root f64 (vsqrt) // we take average latency
               OpDesc(opClass='SimdReduceAdd', opLat=10), # SVE reduction, arithmetic, S form (saddv) 
               OpDesc(opClass='SimdReduceAlu', opLat=12), # SVE reduction, logical (andv)
               OpDesc(opClass='SimdReduceCmp', opLat=9), # SVE reduction, arithmetic, S form (smaxv)
               OpDesc(opClass='SimdFloatReduceAdd', opLat=8, pipelined=False), # SVE floating point associative add (fadda) // Same class for faddv, bad Gem5 implementation
               OpDesc(opClass='SimdFloatReduceCmp', opLat=9), # SVE floating point reduction f64 (fmaxv)
               OpDesc(opClass='FloatAdd', opLat=2), # Aarch64 FP arithmetic (fadd)
               OpDesc(opClass='FloatCmp', opLat=2), # Aarch64 FP compare (fccmpe)
               OpDesc(opClass='FloatCvt', opLat=3), # Aarch64 Fp convert (vcvt)
               OpDesc(opClass='FloatDiv', opLat=11, pipelined=False), # Aarch64 Fp divide (vdiv) // average latency
               OpDesc(opClass='FloatSqrt', opLat=12, pipelined=False), # Aarch64 Fp square root D-form (fsqrt) // average latency
               OpDesc(opClass='FloatMultAcc', opLat=4), # Aarch64 Fp multiply accumulate (vfma)
               OpDesc(opClass='FloatMisc', opLat=3), # Aarch64 miscelleaneaus
               OpDesc(opClass='FloatMult', opLat=3) ] # Aarch64 Fp multiply (fmul)

    count = 2 

# This class refers to pipelines Branch0, Integer single Cycles 0, Integer single Cycle 1 (symbol B and S in (2) table 3)
class O3_ARM_Neoverse_N1_Simple_Int(FUDesc):
    opList = [ OpDesc(opClass='IntAlu', opLat=1) ] # Aarch64 ALU (Unfortunately branches are put together with IntALU :(
    count = 3 # 

# This class refers to pipelines integer single/multicycle 1 (this refers to pipeline symbol M in (2) table 3)
class O3_ARM_Neoverse_N1_Complex_Int(FUDesc):
    opList = [ OpDesc(opClass='IntAlu', opLat=1), # Aarch64 Int ALU
               OpDesc(opClass='IntMult', opLat=2), # Aarch64 Int mult
               OpDesc(opClass='IntDiv', opLat=9, pipelined=False), # Aarch64 Int divide W-form (sdiv) // we take average
               OpDesc(opClass='IprAccess', opLat=1) ] # Aarch64 Prefetch
    count = 1 # 1 units

# This class refers to Load/Store0/1 (symbol L in Neoverse guide table 3-1)
class O3_ARM_Neoverse_N1_LoadStore(FUDesc):
    opList = [ OpDesc(opClass='MemRead'), 
               OpDesc(opClass='FloatMemRead'),
               OpDesc(opClass='MemWrite'),
               OpDesc(opClass='FloatMemWrite') ]
    count = 2 #

class O3_ARM_Neoverse_N1_PredAlu(FUDesc):
    opList = [ OpDesc(opClass='SimdPredAlu')  ]
    count = 1


class O3_ARM_Neoverse_N1_FUP(FUPool):
    FUList = [O3_ARM_Neoverse_N1_Simple_Int(),
              O3_ARM_Neoverse_N1_Complex_Int(),
              O3_ARM_Neoverse_N1_LoadStore(),
              O3_ARM_Neoverse_N1_PredAlu(),
              O3_ARM_Neoverse_N1_FP()]

# Bi-Mode Branch Predictor
class O3_ARM_Neoverse_N1_BP(BiModeBP):
    globalPredictorSize = 8192
    globalCtrBits = 2
    choicePredictorSize = 8192
    choiceCtrBits = 2
    BTBEntries = 4096
    BTBTagSize = 18
    RASSize = 16
    instShiftAmt = 2

class O3_ARM_Neoverse_N1(DerivO3CPU):
    decodeToFetchDelay = 1
    renameToFetchDelay = 1
    iewToFetchDelay = 1
    commitToFetchDelay = 1
    renameToDecodeDelay = 1
    iewToDecodeDelay = 1
    commitToDecodeDelay = 1
    iewToRenameDelay = 1
    commitToRenameDelay = 1
    commitToIEWDelay = 1
    fetchWidth = 4 # taken from source 1.
    fetchBufferSize = 64
    fetchToDecodeDelay = 1
    decodeWidth = 4 # taken from source 1.
    decodeToRenameDelay = 1
    renameWidth = 8 # taken from (1)
    renameToIEWDelay = 1
    issueToExecuteDelay = 1
    dispatchWidth = 8
    issueWidth = 8 # taken from (1)
    wbWidth = 8
    iewToCommitDelay = 1
    renameToROBDelay = 1
    commitWidth = 8
    squashWidth = 8
    trapLatency = 13
    backComSize = 5
    forwardComSize = 5

    numROBEntries = 128 # taken from (1) 
    numPhysFloatRegs = 128 # taken from (4)
    numPhysVecRegs = 128 # taken from (4) 
    numPhysIntRegs = 120 # taken from (4) 

    numIQEntries = 120 # taken from (1)

    fuPool = O3_ARM_Neoverse_N1_FUP()

    switched_out = False
    branchPred = O3_ARM_Neoverse_N1_BP()

    LQEntries = 68 # taken from (1) 
    SQEntries = 72 # taken from (1) 
    LSQDepCheckShift = 0
    LFSTSize = 1024
    SSITSize = 1024

