#!/bin/bash
set -e

if [ -z "$1" ]; then
    echo "================================================="
    echo "用法 1: ./run_experiment.sh <数据量Bytes> (例如 8192, 8388608)"
    echo "用法 2: ./run_experiment.sh stress        (执行随机压测)"
    echo "================================================="
    exit 1
fi

MODE=$1

if [ "$MODE" == "stress" ]; then
    echo ">>> 开始执行实验: 随机访存压测 (Stress Test) <<<"
    DDR4_OUT="results_ddr4/stress"
    HBM2_OUT="results_hbm2/stress"
    mkdir -p "$DDR4_OUT" "$HBM2_OUT"
    
    echo "[*] 运行 DDR4 压测..."
    ./DRAMSim3/build/dramsim3main DRAMSim3/configs/DDR4_8Gb_x8_2400.ini -s random -c 1000000 -o "$DDR4_OUT" > /dev/null
    echo "[*] 运行 HBM2 压测..."
    ./DRAMSim3/build/dramsim3main DRAMSim3/configs/HBM2_8Gb_x128.ini -s random -c 1000000 -o "$HBM2_OUT" > /dev/null
    
    python3 plot_results.py -n stress
else
    N=$MODE
    TRACE_DIR="traces/$N"
    DDR4_OUT="results_ddr4/$N"
    HBM2_OUT="results_hbm2/$N"

    echo ">>> 开始执行实验: 线性流访存, 数据量 = $N Bytes <<<"
    mkdir -p "$TRACE_DIR" "$DDR4_OUT" "$HBM2_OUT"

    echo "[*] 调用 gen_trace.py 生成线性 Trace..."
    python3 gen_trace.py -n "$N" -d "$TRACE_DIR"

    TRACE_FILE="$TRACE_DIR/stream_${N}.trace"
    
    if [ ! -f "$TRACE_FILE" ]; then
        echo "[!] 致命错误: 未能找到生成的 Trace 文件 $TRACE_FILE ！"
        exit 1
    fi

    echo "[*] 运行 DDR4 基准测试..."
    ./DRAMSim3/build/dramsim3main DRAMSim3/configs/DDR4_8Gb_x8_2400.ini -t "$TRACE_FILE" -o "$DDR4_OUT" > /dev/null

    echo "[*] 运行 HBM2 实验组..."
    ./DRAMSim3/build/dramsim3main DRAMSim3/configs/HBM2_8Gb_x128.ini -t "$TRACE_FILE" -o "$HBM2_OUT" > /dev/null

    python3 plot_results.py -n "$N"
fi
echo "================= 测试完成 ================="
