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

#修改内存地址空间为1024KiB

# Define the simulation components
cpu0 = sst.Component("core0", "memHierarchy.standardCPU")
cpu0.addParams({
    "memFreq" : 1,
    "memSize" : "1GiB",
    "verbose" : 0,
    "clock" : "1GHz",
    "rngseed" : 6,
    "maxOutstanding" : 16,
    "opCount" : 10,
    "reqsPerIssue" : 3,
    "write_freq" : 40, # 36% writes
    "read_freq" : 60,  # 60% reads
})
iface0 = cpu0.setSubComponent("memory", "memHierarchy.standardInterface")


cpu1 = sst.Component("core1", "memHierarchy.standardCPU")
cpu1.addParams({
    "memFreq" : 1,
    "memSize" : "16384KiB",
    "verbose" : 0,
    "clock" : "1GHz",
    "rngseed" : 6,
    "maxOutstanding" : 16,
    "opCount" : 10,
    "reqsPerIssue" : 3,
    "write_freq" : 20, # 20% writes
    "read_freq" : 80,  # 80% reads
})
iface1 = cpu1.setSubComponent("memory", "memHierarchy.standardInterface")



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
    "addr_range_end": 8*1024*1024-1,
    "controller_id" : 0,
    "controller_number_per_node" : 2,
})

memory0 = memctrl0.setSubComponent("backend", "memHierarchy.simpleMem")
memory0.addParams({
      "mem_size" : "8192KiB",
      "access_time" : "100 ns",
      "core_num" : 2,
})

print('hello')# 控制器1
memctrl1 = sst.Component("memory1", "memHierarchy.MemController")
memctrl1.addParams({
    "debug" : DEBUG_MEM,
    "debug_level" : 10,
    "clock" : "1GHz",
    #"cpulink.debug" : 1,
    #"cpulink.debug_level" : 10,
    "addr_range_start": 8*1024*1024,
    "addr_range_end": 16*1024*1024-1,
    "controller_id" : 1,
    "controller_number_per_node" : 2,
})

memory1 = memctrl1.setSubComponent("backend", "memHierarchy.simpleMem")
memory1.addParams({
      "mem_size" : "8192KiB",
      "access_time" : "100 ns",
      "core_num" : 2,
})

# Enable statistics
sst.setStatisticLoadLevel(7)
sst.setStatisticOutput("sst.statOutputConsole")
for a in componentlist:
    sst.enableAllStatisticsForComponentType(a)


link_cpu0_bus_link = sst.Link("link_cpu0_bus_link")
link_cpu0_bus_link.connect( (iface0, "port", "1001ps"), (bus, "high_network_0", "1002ps") )
link_cpu1_bus_link = sst.Link("link_cpu1_bus_link")
link_cpu1_bus_link.connect( (iface1, "port", "1003ps"), (bus, "high_network_1", "1004ps") )


# 控制器0
link_bus_mem_link0 = sst.Link("link_bus_mem_link_0")
link_bus_mem_link0.connect( (bus, "low_network_0", "10001ps"), (memctrl0, "direct_link", "10002ps") )
# 控制器1
link_bus_mem_link1 = sst.Link("link_bus_mem_link_1")
link_bus_mem_link1.connect( (bus, "low_network_1", "10003ps"), (memctrl1, "direct_link", "10004ps") )

