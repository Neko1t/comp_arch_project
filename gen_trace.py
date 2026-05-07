import os
import argparse

def generate_linear_stream_trace(N_bytes, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 命名为 stream_N.trace
    output_file = os.path.join(output_dir, f"stream_{N_bytes}.trace")
    
    # 假设 L1 Cache 每次抓取 64 字节
    CACHE_LINE_SIZE = 64
    
    # 设定 A, B, C 三个数组的内存基址，错开足够远防止相互踩踏
    base_A = 0x10000000
    base_B = base_A + N_bytes * 2
    base_C = base_B + N_bytes * 2

    print(f"[*] 正在生成纯线性访存轨迹: {N_bytes} Bytes -> {output_file}")

    req_count = 0
    ISSUE_RATE = 8 # 保持 8 并发，模拟现代处理器发射率

    with open(output_file, 'w') as f:
        # 每次步进 64 字节，模拟最纯粹的顺次 Cache Miss
        for offset in range(0, N_bytes, CACHE_LINE_SIZE):
            cycle = req_count // ISSUE_RATE
            f.write(f"{hex(base_A + offset)} READ {cycle}\n")
            req_count += 1
            
            cycle = req_count // ISSUE_RATE
            f.write(f"{hex(base_B + offset)} READ {cycle}\n")
            req_count += 1
            
            cycle = req_count // ISSUE_RATE
            f.write(f"{hex(base_C + offset)} WRITE {cycle}\n")
            req_count += 1

    print(f"[*] 轨迹生成完毕。总请求数: {req_count}")
    return output_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # 这里的 -n 不再是矩阵维度，而是纯粹的字节数 (Bytes)
    parser.add_argument('-n', '--size', type=int, required=True, help='数据总大小 (Bytes)')
    parser.add_argument('-d', '--dir', type=str, default='traces', help='存放轨迹的目录')
    args = parser.parse_args()
    generate_linear_stream_trace(args.size, args.dir)
