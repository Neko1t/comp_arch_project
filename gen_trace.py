import os
import argparse

def generate_matmul_trace(N, output_dir):
    """
    生成 N x N 矩阵乘法的内存轨迹，并存放到指定目录。
    """
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    output_file = os.path.join(output_dir, f"matmul_{N}x{N}.trace")
    element_size = 4  
    base_A = 0x10000000
    base_B = base_A + (N * N * element_size)
    base_C = base_B + (N * N * element_size)

    print(f"[*] 正在生成轨迹: {N}x{N} -> {output_file}")
    
    with open(output_file, 'w') as f:
        for i in range(N):
            for j in range(N):
                for k in range(N):
                    f.write(f"{hex(base_A + (i * N + k) * element_size)} READ\n")
                    f.write(f"{hex(base_B + (k * N + j) * element_size)} READ\n")
                f.write(f"{hex(base_C + (i * N + j) * element_size)} WRITE\n")
                
    print(f"[*] 轨迹生成完毕。")
    return output_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--size', type=int, required=True, help='矩阵维度 N')
    parser.add_argument('-d', '--dir', type=str, default='traces', help='存放轨迹的目录')
    args = parser.parse_args()
    
    generate_matmul_trace(args.size, args.dir)
