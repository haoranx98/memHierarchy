import random
import argparse

def generate_trace(num_lines, total_mem_gib, output_path, hot_ratio=0.8):
    lines_hot = int(num_lines * 10* hot_ratio)
    num_lines = num_lines * 4
    lines_cold = num_lines - lines_hot

    lines_per_hot_region = lines_hot // 2

    begin = random.uniform(0.25, 0.45)
    end = random.uniform(0.35, 0.55)

    middle = 1 - begin - end

    one_gib = 0x40000000
    print(hex(one_gib))
    total_bytes = total_mem_gib * 1024 * 1024 * 1024
    last_gib_start = total_bytes - one_gib
    print(hex(last_gib_start))
    with open(output_path, "w") as f:
        # 热点区域1：前1GiB内随机分布（密集）
        for _ in range(int(num_lines * begin)):
            addr = random.randint(0, one_gib - 1)
            addr_str = f"{addr & 0xFFFFFFFF:08x}"
            op = random.choice(["lw", "sw"])
            f.write(f"{addr_str}{op}\n")

        # 冷区域：中间部分随机
        for _ in range(int(num_lines * middle)):
            addr = random.randint(one_gib, last_gib_start - 1)
            addr_str = f"{addr & 0xFFFFFFFF:08x}"
            op = random.choice(["lw", "sw"])
            f.write(f"{addr_str}{op}\n")

        # 热点区域2：最后1GiB内随机分布（密集）
        for _ in range(int(num_lines * end)):
            addr = random.randint(last_gib_start, total_bytes - 1)
            addr_str = f"{addr & 0xFFFFFFFF:08x}"
            op = random.choice(["lw", "sw"])
            f.write(f"{addr_str}{op}\n")

    print(f"✅ 已生成 {num_lines} 条访问指令（热点区域随机分布），前后各 {lines_per_hot_region} 条，冷区 {lines_cold} 条")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="生成访存指令（热点区域内随机分布）")
    parser.add_argument("--lines", type=int, default=1000, help="总共生成的行数")
    parser.add_argument("--mem_size", type=int, default=8, help="内存总大小（GiB），默认8GiB")
    parser.add_argument("--output", type=str, default="addr.txt", help="输出文件路径")
    parser.add_argument("--ratio", type=float, default=0.8, help="热点比例（前1GiB和最后1GiB之和），默认0.8")

    args = parser.parse_args()
    generate_trace(args.lines, args.mem_size, args.output, args.ratio)
