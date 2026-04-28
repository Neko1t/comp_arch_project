import os

def generate_matmul_trace(N, output_file):
    """
    模拟 N x N 矩阵乘法 C = A * B 的内存访问轨迹。
    假设矩阵元素为 32位 (4 bytes) 单精度浮点数或整数。
    """
    element_size = 4  # 每个数据占 4 字节
    
    # 为三个矩阵分配模拟的基址 (Base Addresses)
    # 避免地址重叠，这里设置足够大的地址间隔
    base_A = 0x10000000
    base_B = base_A + (N * N * element_size)
    base_C = base_B + (N * N * element_size)

    print(f"开始生成 {N}x{N} 矩阵乘法的内存轨迹...")
    
    with open(output_file, 'w') as f:
        # 经典的 O(N^3) 矩阵乘法循环
        for i in range(N):
            for j in range(N):
                for k in range(N):
                    # 读取矩阵 A[i][k]
                    # A 是按行优先存储的，所以这里是顺序读取
                    addr_A = base_A + (i * N + k) * element_size
                    f.write(f"{hex(addr_A)} READ\n")

                    # 读取矩阵 B[k][j]
                    # B 是按列访问的，这会产生跳跃性的内存地址访问 (Stride Access)
                    # 这种跳跃访问是导致传统DRAM性能下降、体现HBM高带宽优势的关键
                    addr_B = base_B + (k * N + j) * element_size
                    f.write(f"{hex(addr_B)} READ\n")

                # 计算完一个 C[i][j] 的点乘后，将结果写入内存
                addr_C = base_C + (i * N + j) * element_size
                f.write(f"{hex(addr_C)} WRITE\n")
                
    print(f"轨迹生成完毕！文件已保存至: {os.path.abspath(output_file)}")

if __name__ == "__main__":
    # 我们先生成一个 64x64 的小规模矩阵乘法作为初步测试
    # N=64 时，将产生 64*64*64*2 次读操作和 64*64 次写操作，共计约 52.8 万条指令
    matrix_size = 64
    trace_filename = "matmul_64x64.trace"
    
    generate_matmul_trace(matrix_size, trace_filename)
