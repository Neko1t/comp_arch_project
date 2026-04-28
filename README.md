# 计算机架构课程项目：高带宽内存 (HBM) 与传统 DRAM 性能对比分析

## 📖 项目简介
本项目是一个基于模拟器 (Simulation-based) 的计算机架构研究项目，旨在系统性地比较高带宽内存 (HBM) 与传统动态随机存取内存 (DDR4 DRAM) 在处理数据密集型任务时的性能差异。

通过在严格控制的变量环境下（相同的系统参数、相同的测试负载）运行 **DRAMSim3** 周期精确级内存模拟器，本项目量化对比了两种架构在以下三个核心维度的指标：
1. **平均内存访问延迟 (Average Latency)**
2. **系统总功耗 (System Power Consumption)**
3. **内存带宽利用率 (Utilized Bandwidth)**

## 🛠️ 环境依赖与前置准备
本项目在 **Linux (Ubuntu/WSL)** 环境下开发与测试。在运行实验之前，请确保您的系统已安装以下依赖：

### 1. 系统级编译工具
用于编译 DRAMSim3 模拟器：
```bash
sudo apt update
sudo apt install -y build-essential cmake git
```

### 2. Python 虚拟环境 (Conda)
项目包含用于生成内存轨迹 (Trace) 和解析日志作图的 Python 自动化脚本。推荐使用 Conda 隔离环境 ：
```bash
conda create -n dram_env python=3.10 -y
conda activate dram_env
conda install numpy matplotlib -y
```
## 🚀 安装与部署 
请按照以下步骤初始化项目并编译模拟器 ：
```bash
# 1. 克隆本项目
git clone [https://github.com/YourUsername/comp_arch_project.git](https://github.com/YourUsername/comp_arch_project.git)
cd comp_arch_project

# 2. 克隆 DRAMSim3 官方仓库
git clone [https://github.com/umd-memsys/DRAMSim3.git](https://github.com/umd-memsys/DRAMSim3.git)

# 3. 编译 DRAMSim3
cd DRAMSim3
mkdir build && cd build
cmake ..
make -j4
cd ../..
```

## ⚙️ 自动化测试工作流 (Usage)
为了保证实验的完全可复现性，本项目将底层 Trace 生成、DRAMSim3 模拟执行以及 JSON 数据解析作图封装在了一键式自动化 Shell 脚本 run_experiment.sh 中 。

首先，赋予脚本执行权限 ：
```bash
chmod +x run_experiment.sh
```
### 实验一：单线程矩阵乘法测试 (Sequential Access Pattern) 
该模式通过 Python 脚本生成标准的 $O(N^3)$ 矩阵乘法内存访问轨迹，用于测试纯线性、单线程访存下两种架构的表现 。
运行命令： 
```bash
# 运行 N=128 或 256 规模的矩阵运算模拟
./run_experiment.sh 128
```

### 实验二：高并发完全随机压测 (Random Stress Test) 

该模式直接调用 DRAMSim3 内置的 Stream Generator，产生 100 万个周期的极限全地址空间随机读写请求，用于测试架构在严重 Row Buffer Miss 场景下的极端吞吐量 。
运行命令： 
```bash
./run_experiment.sh stress
```
输出结果： 日志将保存至 results_*/stress/ 目录下，并自动生成极端压测对比图 comparison_stress.png 。

## 📁 项目结构
```Plaintext
comp_arch_project/
├── DRAMSim3/               # 内存模拟器源码及配置文件 (DDR4_8Gb_x8_2400.ini, HBM2_8Gb_x128.ini)
├── gen_trace.py            # Python 内存轨迹生成脚本 (支持矩阵乘法)
├── plot_results.py         # 自动化 JSON 日志解析与多子图数据可视化脚本
├── run_experiment.sh       # 端到端自动化实验工作流脚本
├── results_ddr4/           # DDR4 基准测试日志及图表输出目录
├── results_hbm2/           # HBM2 实验组日志输出目录
└── README.md               # 项目说明文档
```