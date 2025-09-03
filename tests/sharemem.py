import sst
import os

current_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(current_dir)
sys.path.append("..")

from mhlib import componentlist

DEBUG_MEM = 0
DEBUG_CORE0 = 0
DEBUG_CORE1 = 0

IS_RECONFIGURE = False
CONTROLLER_NUMBER_PER_NODE = 1
MEM_SIZE = "2GiB"
BLOCK_NUM_PER_CONTROLLER = 1
INPUT_0_FILE_PATH = "/home/zjlab/addr_8_0.txt"
INPUT_1_FILE_PATH = "/home/zjlab/addr_8_1.txt"
OUTPUT_FOLDER_PATH = "/home/zjlab/share_mem"


# Define the simulation components

# cpu0
cpu0 = sst.Component("core0", "memHierarchy.standardCPU")
cpu0.addParams({
    "memFreq": 1,
    "memSize": MEM_SIZE,
    "verbose": 0,
    "clock": "1GHz",
    "rngseed": 6,
    "maxOutstanding" : 16,
    "opCount" : 10,
    "reqsPerIssue" : 3,
    "write_freq" : 40, # 36% writes
    "read_freq" : 60,  # 60% reads
    "mem_data_path": INPUT_0_FILE_PATH
})
iface0 = cpu0.setSubComponent("memory", "memHierarchy.standardInterface")

# cpu1
cpu1 = sst.Component("core1", "memHierarchy.standardCPU")
cpu1.addParams({
    "memFreq": 1,
    "memSize": MEM_SIZE,
    "verbose": 0,
    "clock": "1GHz",
    "rngseed": 6,
    "maxOutstanding" : 16,
    "opCount" : 10,
    "reqsPerIssue" : 3,
    "write_freq" : 40, # 36% writes
    "read_freq" : 60,  # 60% reads
    "mem_data_path": INPUT_1_FILE_PATH
})
iface1 = cpu1.setSubComponent("memory", "memHierarchy.standardInterface")


bus = sst.Component("bus", "memHierarchy.Bus")
bus.addParams({
    "bus_frequency": "4 Ghz",
})

# 循环创建多个控制器和内存模块

memctrl = sst.Component(f"memory", "memHierarchy.MemController")
memctrl.addParams({
    "debug": DEBUG_MEM,
    "debug_level": 10,
    "clock": "1GHz",
    "addr_range_start": 0,
    "addr_range_end": 1024 * 1024 * 1024- 1,
    "controller_id": 0,
    "controller_number_per_node": CONTROLLER_NUMBER_PER_NODE,
    "block_num_per_controller" : BLOCK_NUM_PER_CONTROLLER,
    "isConfigured": IS_RECONFIGURE,
    "isShared": False,
    "output_folder_path": OUTPUT_FOLDER_PATH
})

memory = memctrl.setSubComponent("backend", "memHierarchy.simpleMem")
memory.addParams({
    "mem_size": "1024MiB",
    "access_time": "100 ns",
})

   

# Enable statistics
sst.setStatisticLoadLevel(7)
sst.setStatisticOutput("sst.statOutputConsole")
for a in componentlist:
    sst.enableAllStatisticsForComponentType(a)


# cpu0
link_cpu0_bus_link = sst.Link("link_cpu0_bus_link")
link_cpu0_bus_link.connect((iface0, "port", "1000ps"), (bus, "high_network_0", "1000ps"))

# cpu1
link_cpu1_bus_link = sst.Link("link_cpu1_bus_link")
link_cpu1_bus_link.connect((iface1, "port", "1000ps"), (bus, "high_network_1", "1000ps"))

link_bus_mem_link = sst.Link("link_bus_mem_link")
link_bus_mem_link.connect((bus, "low_network_0", "1000ps"), (memctrl, "direct_link", "1000ps"))

