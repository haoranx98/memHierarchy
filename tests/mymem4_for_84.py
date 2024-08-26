import sst
import os

current_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(current_dir)
sys.path.append("..")

from mhlib import componentlist

DEBUG_MEM = 0
DEBUG_CORE0 = 0
DEBUG_CORE1 = 0

IS_RECONFIGURE = True
CONTROLLER_NUMBER_PER_NODE = 8
BLOCK_NUM_PER_CONTROLLER = 16
OUTPUT_FOLDER_PATH = "/home/haoranx98/sst"

# 修改内存地址空间为1024KiB

# Define the simulation components
cpu = sst.Component("core", "memHierarchy.standardCPU")
cpu.addParams({
    "memFreq": 1,
    "memSize": "8GiB",
    "verbose": 0,
    "clock": "1GHz",
    "rngseed": 6,
    "maxOutstanding": 16,
    "opCount": 10,
    "reqsPerIssue": 3,
    "write_freq": 40,  # 36% writes
    "read_freq": 60,   # 60% reads
    # "mem_data_path": "/home/haoranx98/addr_GAN.txt"
    "mem_data_path": "/home/haoranx98/Documents/GAN/perf_addr/addr_GAN_1024.txt"
})
iface = cpu.setSubComponent("memory", "memHierarchy.standardInterface")

bus = sst.Component("bus", "memHierarchy.Bus")
bus.addParams({
    "bus_frequency": "4 Ghz",
})

# 循环创建多个控制器和内存模块
for i in range(CONTROLLER_NUMBER_PER_NODE):
    memctrl = sst.Component(f"memory{i}", "memHierarchy.MemController")
    memctrl.addParams({
        "debug": DEBUG_MEM,
        "debug_level": 10,
        "clock": "1GHz",
        "addr_range_start": i * 1024 * 1024 * 1024,
        "addr_range_end": (i + 1) * 1024 * 1024 * 1024- 1,
        "controller_id": i,
        "controller_number_per_node": CONTROLLER_NUMBER_PER_NODE,
        "block_num_per_controller" : BLOCK_NUM_PER_CONTROLLER,
        "isConfigured": IS_RECONFIGURE,
        "output_folder_path": OUTPUT_FOLDER_PATH
    })

    memory = memctrl.setSubComponent("backend", "memHierarchy.simpleMem")
    memory.addParams({
        "mem_size": "1024MiB",
        "access_time": "100 ns",
    })

    # Connect each memory controller to the bus
    link_bus_mem_link = sst.Link(f"link_bus_mem_link_{i}")
    link_bus_mem_link.connect((bus, f"low_network_{i}", f"1000{i + 2}ps"), (memctrl, "direct_link", f"1000{i + 3}ps"))

# Enable statistics
sst.setStatisticLoadLevel(7)
sst.setStatisticOutput("sst.statOutputConsole")
for a in componentlist:
    sst.enableAllStatisticsForComponentType(a)

link_cpu_bus_link = sst.Link("link_cpu_bus_link")
link_cpu_bus_link.connect((iface, "port", "1001ps"), (bus, "high_network_0", "1002ps"))
