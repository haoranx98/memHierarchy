import sst
import os
current_dir = os.path.abspath(os.path.dirname(__file__))
# print(current_dir)
sys.path.append(current_dir)
sys.path.append("..")

from mhlib import componentlist

DEBUG_MEM = 0
DEBUG_CORE0 = 0
DEBUG_CORE1 = 0

IS_RECONFIGURE = True
CONTROLLER_NUMBER_PER_NODE = 2
OUTPUT_FOLDER_PATH = "/home/haoranx98/sst"

#修改内存地址空间为1024KiB

# Define the simulation components
cpu = sst.Component("core", "memHierarchy.standardCPU")
cpu.addParams({
    "memFreq" : 1,
    "memSize" : "8GiB",
    "verbose" : 0,
    "clock" : "1GHz",
    "rngseed" : 6,
    "maxOutstanding" : 16,
    "opCount" : 10,
    "reqsPerIssue" : 3,
    "write_freq" : 40, # 36% writes
    "read_freq" : 60,  # 60% reads
    "mem_data_path": "/home/haoranx98/addr.txt"
})
iface = cpu.setSubComponent("memory", "memHierarchy.standardInterface")

bus = sst.Component("bus", "memHierarchy.Bus")
bus.addParams({
      "bus_frequency" : "4 Ghz",
})

# 控制器0
memctrl0 = sst.Component("memory0", "memHierarchy.MemController")
memctrl0.addParams({
    "debug" : DEBUG_MEM,
    "debug_level" : 10,
    "clock" : "1GHz",
    #"cpulink.debug" : 1,
    #"cpulink.debug_level" : 10,
    "addr_range_start": 0,
    "addr_range_end": 4*1024*1024*1024-1,
    "controller_id" : 0,
    "controller_number_per_node" : CONTROLLER_NUMBER_PER_NODE,
    "isConfigured" : IS_RECONFIGURE,
    "output_folder_path" : OUTPUT_FOLDER_PATH
})

memory0 = memctrl0.setSubComponent("backend", "memHierarchy.simpleMem")
memory0.addParams({
      "mem_size" : "4GiB",
      "access_time" : "100 ns",
})

memctrl1 = sst.Component("memory1", "memHierarchy.MemController")
memctrl1.addParams({
    "debug" : DEBUG_MEM,
    "debug_level" : 10,
    "clock" : "1GHz",
    #"cpulink.debug" : 1,
    #"cpulink.debug_level" : 10,
    "addr_range_start": 4*1024*1024*1024,
    "addr_range_end": 8*1024*1024*1024-1,
    "controller_id" : 1,
    "controller_number_per_node" : CONTROLLER_NUMBER_PER_NODE,
    "isConfigured" : IS_RECONFIGURE,
    "output_folder_path" : OUTPUT_FOLDER_PATH
})

memory1 = memctrl1.setSubComponent("backend", "memHierarchy.simpleMem")
memory1.addParams({
      "mem_size" : "4GiB",
      "access_time" : "100 ns",
})

# Enable statistics
sst.setStatisticLoadLevel(7)
sst.setStatisticOutput("sst.statOutputConsole")
for a in componentlist:
    sst.enableAllStatisticsForComponentType(a)


link_cpu_bus_link = sst.Link("link_cpu_bus_link")
link_cpu_bus_link.connect( (iface, "port", "1001ps"), (bus, "high_network_0", "1002ps") )


# 控制器0
link_bus_mem_link0 = sst.Link("link_bus_mem_link_0")
link_bus_mem_link0.connect( (bus, "low_network_0", "10001ps"), (memctrl0, "direct_link", "10002ps") )
# 控制器1
link_bus_mem_link1 = sst.Link("link_bus_mem_link_1")
link_bus_mem_link1.connect( (bus, "low_network_1", "10003ps"), (memctrl1, "direct_link", "10004ps") )

