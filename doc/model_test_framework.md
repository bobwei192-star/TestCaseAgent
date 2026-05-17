给你的建议
结合你想做的 “ROCm + PyTorch + vLLM” 镜像推理场景，可以参考这个路径来选型：

优先参考 GenAIEval：它的设计很贴近你的需求——直接针对AI推理服务的吞吐量/延迟做性能基准测试，而且基于YAML配置测试用例。这和你的Agent自动生成YAML的思路高度一致。

用 ELM 的理念做工程化：你的test-case-agent要保证每次测试结果可信，就得学ELM的设计——把模型版本、环境配置、随机种子这些都固化下来，确保可复现。这能成为你Agent的一个核心亮点。

集成 HELM 或 OpenCompass 跑分：当你需要对外展示模型能力时，可以直接用这两个框架的标准数据集跑分。你的Agent可以设计成一个自动调用它们的调度器。

你的test-case-agent如果想先聚焦性能测试（吞吐量/延迟），GenAIEval的YAML配置方式很有参考价值；如果未来想扩展到模型效果评估，OpenCompass和HELM会是很好的对标框架。需要我进一步分析某个框架的技术架构，看看怎么集成到你的Agent里吗？

针对 ROCm + PyTorch + vLLM 推理镜像 的测试需求，你需要的是推理服务端点测试框架，而非训练阶段的模型评估。以下是匹配你场景的开源/标准方案：
一、推理端点性能与正确性测试
表格
框架	定位	是否开源	核心能力	适配你的场景
vLLM 自带 Benchmark 工具	官方性能测试	✅ Apache 2.0	测 TTFT、TPOT、吞吐量、并发压力	必用，直接内置于 vLLM，支持 ROCm
Agentic Swarm Bench (ASB)	Agent 负载模拟	✅ 开源	模拟 32+ 并发 Agent 长上下文负载，输出 JSON 供 CI 解析	强烈推荐，正好匹配你的 Agent CI 场景
ROCm MAD (Model Automation & Dashboarding)	AMD 官方基准	✅ 开源	AMD 官方维护的 Docker 化 benchmark，支持 vLLM + ROCm 组合	必用，直接跑在 ROCm 容器内
1. vLLM 自带工具（最基础）
vLLM 内置了 benchmark_serving.py 和 benchmark_throughput.py，可以直接对启动好的服务端点施压：
bash
复制
# 先启动你的 ROCm+vLLM 容器
docker run -d --device=/dev/kfd --device=/dev/dri ... your-image

# 压测端点
python benchmark_serving.py \
  --backend vllm \
  --dataset-name sharegpt \
  --model /path/to/model \
  --num-prompts 1000 \
  --request-rate 10
输出 TTFT（首 token 延迟）、ITL（token 间延迟）、吞吐量等关键指标。
2. Agentic Swarm Bench（Agent 场景专用）
这是专门测Agent 工作负载下推理性能的框架，支持模拟多 Agent 并发、长上下文累积（6K→100K tokens）：
bash
复制
# 测 32 并发 Agent 在长上下文下的表现
asb speed -e http://localhost:8000 -m your-model -u 32 -p long --format json -o results.json
输出 JSON 直接喂给 CI pipeline，适合你的"AI Agent 修复后自动验证"闭环。
3. ROCm MAD（AMD 官方基准）
AMD 官方维护的 Docker 化测试框架，已经预配置好 ROCm + vLLM 组合：
bash
复制
git clone https://github.com/ROCm/MAD
cd MAD
pip install -r requirements.txt

# 跑 DBRX FP8 性能测试
export MAD_SECRETS_HFTOKEN="your_token"
python3 tools/run_models.py --tags pyt_vllm_dbrx_fp8 --keep-model-dir --live-output
报告自动生成在 ~/MAD/reports_float8/，包含延迟和吞吐量数据。