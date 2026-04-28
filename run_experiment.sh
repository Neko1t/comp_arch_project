#!/bin/bash
set -e

# 检查输入参数
if [ -z "$1" ]; then
    echo "================================================="
    echo "用法 1: ./run_experiment.sh <矩阵大小N> (例如 64, 128)"
    echo "用法 2: ./run_experiment.sh stress        (执行随机压测)"
    echo "================================================="
    exit 1
fi

MODE=$1

if [ "$MODE" == "stress" ]; then
    echo ">>> 开始执行实验: 高并发随机压测 (Stress Test) <<<"
    
    DDR4_OUT="results_ddr4/stress"
    HBM2_OUT="results_hbm2/stress"
    
    # 建立压测结果专属文件夹
    mkdir -p "$DDR4_OUT" "$HBM2_OUT"
    
    echo "[*] 运行 DDR4 压测 (生成 100万 个周期的极限读写流)..."
    ./DRAMSim3/build/dramsim3main DRAMSim3/configs/DDR4_8Gb_x8_2400.ini -s random -c 1000000 -o "$DDR4_OUT" > /dev/null
    
    echo "[*] 运行 HBM2 压测 (激活 8 通道并行)..."
    ./DRAMSim3/build/dramsim3main DRAMSim3/configs/HBM2_8Gb_x128.ini -s random -c 1000000 -o "$HBM2_OUT" > /dev/null
    
    echo "[*] 正在解析数据并生成压测对比图..."
    python plot_results.py -n stress

else
    # 验证输入是否为纯数字
    if ! [[ "$MODE" =~ ^[0-9]+$ ]]; then
        echo "错误: 参数必须是有效的数字 (矩阵维度) 或 'stress'"
        exit 1
    fi
    
    N=$MODE
    TRACE_DIR="traces/$N"
    DDR4_OUT="results_ddr4/$N"
    HBM2_OUT="results_hbm2/$N"

    echo ">>> 开始执行实验: 单线程矩阵乘法 N = $N <<<"

    mkdir -p "$TRACE_DIR" "$DDR4_OUT" "$HBM2_OUT"

    python gen_trace.py -n "$N" -d "$TRACE_DIR"
    TRACE_FILE="$TRACE_DIR/matmul_${N}x${N}.trace"

    echo "[*] 运行 DDR4 基准测试..."
    ./DRAMSim3/build/dramsim3main DRAMSim3/configs/DDR4_8Gb_x8_2400.ini -t "$TRACE_FILE" -o "$DDR4_OUT" > /dev/null

    echo "[*] 运行 HBM2 实验组..."
    ./DRAMSim3/build/dramsim3main DRAMSim3/configs/HBM2_8Gb_x128.ini -t "$TRACE_FILE" -o "$HBM2_OUT" > /dev/null

    echo "[*] 正在解析数据并生成单线程对比图..."
    python plot_results.py -n "$N"
fi

echo "=================================================="
echo " 当前测试流程已全部自动完成！"
echo "=================================================="
