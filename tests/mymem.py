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
    "memSize" : "1024KiB",
    "verbose" : 0,
    "clock" : "1GHz",
    "rngseed" : 6,
    "maxOutstanding" : 16,
    "opCount" : 2,
    "reqsPerIssue" : 3,
    "write_freq" : 40, # 36% writes
    "read_freq" : 60,  # 60% reads
})
iface0 = cpu0.setSubComponent("memory", "memHierarchy.standardInterface")


cpu1 = sst.Component("core1", "memHierarchy.standardCPU")
cpu1.addParams({
    "memFreq" : 1,
    "memSize" : "1024KiB",
    "verbose" : 0,
    "clock" : "1GHz",
    "rngseed" : 6,
    "maxOutstanding" : 16,
    "opCount" : 2,
    "reqsPerIssue" : 3,
    "write_freq" : 20, # 20% writes
    "read_freq" : 80,  # 80% reads
})
iface1 = cpu1.setSubComponent("memory", "memHierarchy.standardInterface")



bus = sst.Component("bus", "memHierarchy.Bus")
bus.addParams({
      "bus_frequency" : "4 Ghz",
})


memctrl = sst.Component("memory", "memHierarchy.MemController")
memctrl.addParams({
    "debug" : DEBUG_MEM,
    "debug_level" : 10,
    "clock" : "1GHz",
    #"cpulink.debug" : 1,
    #"cpulink.debug_level" : 10,
    "addr_range_end" : 512*1024*1024-1,
})

memory = memctrl.setSubComponent("backend", "memHierarchy.simpleMem")
memory.addParams({
      "mem_size" : "2048KiB",
      "access_time" : "100 ns",
      "core_num" : 2,
})

# Enable statistics
sst.setStatisticLoadLevel(7)
sst.setStatisticOutput("sst.statOutputConsole")
for a in componentlist:
    sst.enableAllStatisticsForComponentType(a)


link_cpu0_bus_link = sst.Link("link_cpu0_bus_link")
link_cpu0_bus_link.connect( (iface0, "port", "1000ps"), (bus, "high_network_0", "1000ps") )
link_cpu1_bus_link = sst.Link("link_cpu1_bus_link")
link_cpu1_bus_link.connect( (iface1, "port", "1000ps"), (bus, "high_network_1", "1000ps") )
link_bus_mem_link = sst.Link("link_bus_mem_link")
link_bus_mem_link.connect( (bus, "low_network_0", "10000ps"), (memctrl, "direct_link", "10000ps") )


