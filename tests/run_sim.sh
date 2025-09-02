#!/bin/bash

# 默认参数
CONTROLLER_NUM=8
BLOCK_NUM=16
INPUT_FILE="/home/zjlab/addr.txt"
OUTPUT_FOLDER="/home/zjlab/sst/"
IS_RECONFIGURE="True"
FORCE_GENERATE=false

# 设置生成行数、读写比例等参数
TRACE_LINES=2000
TRACE_RATIO=0.75



# 模板路径
TEMPLATE_FILE="/home/zjlab/scratch/src/sstelements-13.1.0/src/sst/elements/memHierarchy/tests/reconfigure_2_2.py"

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --controller_num)
            CONTROLLER_NUM="$2"
            shift 2
            ;;
        --block_num)
            BLOCK_NUM="$2"
            shift 2
            ;;
        --input)
            INPUT_FILE="$2"
            shift 2
            ;;
        --output)
            OUTPUT_FOLDER="$2"
            shift 2
            ;;
        --reconfigure)
            IS_RECONFIGURE="$2"
            shift 2
            ;;
        --force_generate)
            FORCE_GENERATE=true
            shift
            ;;
        *)
            echo "❌ 未知参数: $1"
            exit 1
            ;;
    esac
done

# 自动计算 MEM_SIZE，例如 CONTROLLER_NUM=8 => 8GiB
MEM_SIZE="${CONTROLLER_NUM}GiB"

# 输出 Python 文件路径
TARGET_DIR=$(dirname "$TEMPLATE_FILE")
TARGET_FILE="${TARGET_DIR}/reconfigure_${CONTROLLER_NUM}_${BLOCK_NUM}.py"
RESULT_TXT="${OUTPUT_FOLDER}/reconfigure_${CONTROLLER_NUM}_${BLOCK_NUM}.txt"

echo $RESULT_TXT

# 创建输出目录（如果不存在）
mkdir -p "$TARGET_DIR"

# 若目标脚本已存在且未强制重建，直接运行 SST
if [[ -f "$TARGET_FILE" && "$FORCE_GENERATE" == false ]]; then
    echo "✅ 配置脚本已存在，跳过生成: $TARGET_FILE"
else
    # 拷贝模板并替换参数
    cp "$TEMPLATE_FILE" "$TARGET_FILE"

    sed -i "s|^IS_RECONFIGURE *=.*|IS_RECONFIGURE = ${IS_RECONFIGURE}|" "$TARGET_FILE"
    sed -i "s|^CONTROLLER_NUMBER_PER_NODE *=.*|CONTROLLER_NUMBER_PER_NODE = ${CONTROLLER_NUM}|" "$TARGET_FILE"
    sed -i "s|^BLOCK_NUM_PER_CONTROLLER *=.*|BLOCK_NUM_PER_CONTROLLER = ${BLOCK_NUM}|" "$TARGET_FILE"
    sed -i "s|^INPUT_FILE_PATH *=.*|INPUT_FILE_PATH = \"${INPUT_FILE}\"|" "$TARGET_FILE"
    sed -i "s|^OUTPUT_FOLDER_PATH *=.*|OUTPUT_FOLDER_PATH = \"${OUTPUT_FOLDER}\"|" "$TARGET_FILE"
    echo "$(grep '^OUTPUT_FOLDER_PATH' "$TARGET_FILE")"
    sed -i "s|^MEM_SIZE *=.*|MEM_SIZE = \"${MEM_SIZE}\"|" "$TARGET_FILE"

    echo "✅ 已生成配置文件: $TARGET_FILE"
fi

# 自动生成 trace 文件（如果不存在或强制生成）
if [[ "$FORCE_GENERATE" == true || ! -f "$INPUT_FILE" ]]; then
    echo "⚠️ 正在生成 trace 文件: $INPUT_FILE"

    # 提取 MEM_SIZE 中的数字部分（例如 "8GiB" -> 8）
    MEM_SIZE_NUM=$(echo "$MEM_SIZE" | grep -o -E '[0-9]+')



    python3 ./tests/generate_trace.py \
        --lines "$TRACE_LINES" \
        --mem_size "$MEM_SIZE_NUM" \
        --output "$INPUT_FILE" \
        --ratio "$TRACE_RATIO"

    if [ $? -ne 0 ]; then
        echo "❌ Trace 生成失败，退出"
        exit 1
    fi
else
    echo "✅ Trace 文件已存在: $INPUT_FILE"
fi

# 运行 SST 并在成功后执行绘图
echo "🚀 正在运行 SST..."
if sst "$TARGET_FILE"; then
    echo "✅ SST 运行成功"

    # 确保输出结果存在
    if [[ -f "$RESULT_TXT" ]]; then
        echo "📈 正在绘图 map_reorder.py ..."
        python3 tests/map_reorder.py "$RESULT_TXT" "$CONTROLLER_NUM" "$BLOCK_NUM" "$OUTPUT_FOLDER"
    else
        echo "⚠️ 结果文件不存在，跳过绘图: $RESULT_TXT"
    fi
else
    echo "❌ SST 运行失败"
    exit 1
fi
