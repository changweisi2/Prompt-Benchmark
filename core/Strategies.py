STRATEGIES = [
    {
        "name": "_0_CoT",
        "description": "请逐步思考并写出你的链式推理过程，然后给出最终答案"
    },
    {
        "name": "_1_SC",
        "description": "请独立生成 N 次链式推理，并输出所有答案。最后统计出现频率最高的答案并给出最终结果"
    },
    {
        "name": "_2_ToT",
        "description": "步骤1：生成 K 个不同思路。步骤2：为每个思路评分（0-10）。步骤3：选出最高分方案并展开为最终答案"
    },
    {
        "name": "_3_GoT",
        "description": "生成多条解法→分析互补点→融合成最优超级解法"
    },
    {
        "name": "_4_Auto-CoT",
        "description": "对给定任务自动匹配类别→调用对应示例链→生成答案"
    },
    {
        "name": "_5_KGR",
        "description": "请基于你自身具备的知识来进行推理和给出答案"
    },
    {
        "name": "_6_ART",
        "description": "给出解决问题所需要的工具并使用这些工具来解决问题"
    },
    {
        "name": "_7_ReAct",
        "description": "以 [Thought] → [Action] → [Observation] 方式循环，直至得到最终答案"
    },
    {
        "name": "_8_APE",
        "description": "生成多条候选 prompt → 模型自身评估 → 选最优 → 迭代优化"
    },
    {
        "name": "_9_RAG",
        "description": "1. 检索相关信息  2. 基于检索内容回答  3. 给出引用证据"
    }
]