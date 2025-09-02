# 脚本使用说明

运行环境要求

| SST            | 13.1.0     |
| -------------- | ---------- |
| python package | matplotlib |

文件列表

| 脚本名称            | 功能描述                                      | 示例用法                                                     |
| ------------------- | --------------------------------------------- | ------------------------------------------------------------ |
| `run_sim.sh`        | 主控制脚本：自动生成配置、调用 SST 模拟并绘图 | `./run_sim.sh --controller_num 4 --block_num 4 --force_generate` |
| `generate_trace.py` | 生成测试用 trace 文件，格式为地址+操作类型    | `python3 tests/generate_trace.py --lines 2000 --mem_size 4 --output ./addr.txt --ratio 0.75` |
| `map_reorder.py`    | 分析 SST 模拟生成的映射结果文件并绘图         | `python3 tests/map_reorder.py tests/reconfigure_4_4.txt 4 4` |

主要使用**run_sim.sh**进行模拟，其参数列表如下

| 参数名称           | 是否可选 | 默认值                      | 说明                                                         |
| ------------------ | -------- | --------------------------- | ------------------------------------------------------------ |
| `--controller_num` | 是       | 8                           | 每个节点的内存控制器数量，用于生成配置脚本和 trace 地址空间  |
| `--block_num`      | 是       | 16                          | 每个控制器下的块数，用于配置 SST                             |
| `--input`          | 是       | `/home/zjlab/addr.txt`      | 输入 trace 文件路径。如果文件不存在将自动生成                |
| `--output`         | 是       | `/home/zjlab/sst`           | SST 模拟结果输出文件夹路径                                   |
| `--reconfigure`    | 是       | `True`                      | 是否开启重配置功能，影响 SST 配置文件中的 `IS_RECONFIGURE` 参数 |
| `--force_generate` | 是       | `false`（不设置则为 false） | 是否强制重新生成 trace 文件和配置文件，即使目标文件已存在    |

默认运行命令如下

```shell
 ./tests/run_sim.sh --controller_num 4 --block_num 4 --input /home/zjlab/scratch/src/sstelements-13.1.0/src/sst/elements/memHierarchy/tests/addr_4_4.txt
```

