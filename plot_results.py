import json
import os
import argparse
import matplotlib.pyplot as plt
import numpy as np

def extract_metrics(json_path):
    """从 JSON 日志中提取延迟、功耗和带宽数据"""
    if not os.path.exists(json_path):
        print(f"[!] 警告: 找不到文件 {json_path}")
        return 0, 0, 0
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    pwr, bw, read_cmds, lat_sum = 0.0, 0.0, 0, 0.0
    for ch_id, ch_data in data.items():
        pwr += ch_data.get('average_power', 0.0)
        bw += ch_data.get('average_bandwidth', 0.0)
        reads = ch_data.get('num_read_cmds', 0)
        if reads > 0:
            read_cmds += reads
            lat_sum += ch_data.get('average_read_latency', 0.0) * reads
            
    avg_latency = (lat_sum / read_cmds) if read_cmds > 0 else 0.0
    return avg_latency, pwr, bw

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--size', type=str, required=True, help='矩阵大小 N，或者填入 stress')
    args = parser.parse_args()
    N = args.size

    path_ddr4 = f"results_ddr4/{N}/dramsim3.json"
    path_hbm2 = f"results_hbm2/{N}/dramsim3.json"
    output_dir = f"results_ddr4/{N}" 

    print(f"[*] 正在解析模式: {N} 的实验数据...")
    d_lat, d_pwr, d_bw = extract_metrics(path_ddr4)
    h_lat, h_pwr, h_bw = extract_metrics(path_hbm2)

    # ---------------- 核心优化部分：使用独立子图 ----------------
    # 创建 1 行 3 列的画布，长宽比为 15:5.5
    fig, axes = plt.subplots(1, 3, figsize=(15, 5.5))
    
    if N == "stress":
        fig.suptitle('Performance Comparison (Random Stress Test)', fontsize=16, fontweight='bold')
    else:
        fig.suptitle(f'Performance Comparison (Matrix Size: {N}x{N})', fontsize=16, fontweight='bold')

    # 将数据打包，方便循环绘图
    metrics = [
        ('Average Latency (Cycles)', [d_lat, h_lat]),
        ('System Power (mW)', [d_pwr, h_pwr]),
        ('Utilized Bandwidth (GB/s)', [d_bw, h_bw])
    ]
    
    x = np.arange(2)
    width = 0.5
    colors = ['#4A90E2', '#F5A623']
    labels = ['DDR4 Baseline', 'HBM2']
    
    for i, (title, data) in enumerate(metrics):
        ax = axes[i]
        # 绘制柱状图
        bars = ax.bar(x, data, width, color=colors)
        
        ax.set_title(title, fontsize=13)
        ax.set_xticks(x)
        ax.set_xticklabels(labels, fontsize=12)
        
        # 隐藏右侧和顶部的边框（让图表更有高级感）
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        
        # 添加数值标签
        ax.bar_label(bars, padding=4, fmt='%.2f', fontsize=11)
        
        # 动态调高当前子图的 Y 轴上限
        max_val = max(data)
        if max_val > 0:
            ax.set_ylim(0, max_val * 1.15)
    # ------------------------------------------------------------
    
    plt.tight_layout()
    save_path = os.path.join(output_dir, f"comparison_{N}.png")
    plt.savefig(save_path, dpi=300)
    print(f"[+] 优化排版后的对比图表已保存至: {save_path}")

if __name__ == "__main__":
    main()
