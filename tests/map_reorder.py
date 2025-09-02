import sys
import os
import matplotlib.pyplot as plt

def parse_line(line, prefix):
    if not line.startswith(prefix):
        raise ValueError(f"行必须以 '{prefix}' 开头：{line.strip()}")
    parts = line[len(prefix):].strip().split('\t')
    return [int(x) for x in parts if x.strip()]

def print_matrix(title, array, rows, cols):
    print(f"\n{title} ({rows}×{cols}):")
    for i in range(rows):
        row = array[i * cols : (i + 1) * cols]
        print("  " + "\t".join(f"{x:>3}" for x in row))

def get_controller_sums(data, controller_per_node, block_per_controller):
    return [sum(data[i * block_per_controller : (i + 1) * block_per_controller])
            for i in range(controller_per_node)]

def plot_dual_pie_chart(old_sums, new_sums, controller_per_node, block_per_controller, output_path):
    labels = [f"C{i}" for i in range(controller_per_node)]

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    axes[0].pie(old_sums, labels=labels, autopct='%1.1f%%', startangle=140)
    axes[0].set_title("Old Mapping")

    axes[1].pie(new_sums, labels=labels, autopct='%1.1f%%', startangle=140)
    axes[1].set_title("New Mapping")

    plt.suptitle("Controller Block Distribution Comparison")
    plt.tight_layout()

    outfile = os.path.join(output_path, f"block_distribution_{controller_per_node}_{block_per_controller}.png")
    plt.savefig(outfile)
    print(f"✅ 图表已保存为 {outfile}")
    plt.show()

def plot_single_pie_chart(sums, controller_per_node, block_per_controller, output_path):
    labels = [f"C{i}" for i in range(controller_per_node)]
    plt.figure(figsize=(8, 8))
    plt.pie(sums, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title("Block Distribution per Controller (Old Mapping)")
    plt.axis('equal')
    plt.tight_layout()

    outfile = os.path.join(output_path, f"single_pie_chart_{controller_per_node}_{block_per_controller}.png")
    plt.savefig(outfile)
    print(f"✅ 图表已保存为 {outfile}")
    plt.show()
    

# ✅ 参数处理
if len(sys.argv) != 5:
    print("用法: python map_reorder.py <filename> <controller_per_node> <block_per_controller> <output_path>")
    sys.exit(1)

filename = sys.argv[1]
controller_per_node = int(sys.argv[2])
block_per_controller = int(sys.argv[3])
output_path = sys.argv[4]

# 确保路径存在
os.makedirs(output_path, exist_ok=True)

total_blocks = controller_per_node * block_per_controller

# ✅ 读取文件
with open(filename, 'r') as f:
    lines = [line.strip() for line in f if line.strip()]
    if len(lines) == 0:
        print("❌ 错误：文件为空")
        sys.exit(1)

    old = parse_line(lines[0], "old:")
    if len(old) != total_blocks:
        print(f"❌ old 数据长度不符，应为 {total_blocks}，实际为 {len(old)}")
        sys.exit(1)

    print_matrix("Old Mapping", old, controller_per_node, block_per_controller)

    if len(lines) > 1:
        new = parse_line(lines[1], "new:")
        if len(new) != total_blocks:
            print(f"❌ new 数据长度不符，应为 {total_blocks}，实际为 {len(new)}")
            sys.exit(1)

        print_matrix("New Mapping", new, controller_per_node, block_per_controller)

        old_sums = get_controller_sums(old, controller_per_node, block_per_controller)
        new_sums = get_controller_sums(new, controller_per_node, block_per_controller)

        plot_dual_pie_chart(old_sums, new_sums, controller_per_node, block_per_controller, output_path)

    else:
        old_sums = get_controller_sums(old, controller_per_node, block_per_controller)
        plot_single_pie_chart(old_sums, controller_per_node, block_per_controller, output_path)
