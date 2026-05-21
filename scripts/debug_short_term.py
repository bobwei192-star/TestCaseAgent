from src.agent.runner import run_multi_turn

results = run_multi_turn([
    '为 ROCm 基础环境生成 pytest 测试用例，检查 rocm-smi 是否存在',
    '刚才的代码没有捕获 stdout，请修改成捕获 stdout 和 stderr 的方式',
    '再补充一个检查 GPU 温度的测试函数',
], thread_id='test-conversation-001', user_id='zx', project_id='rocm')

print('\n=== 验证短期记忆（MemorySaver）===')

final_state = results[-1]
final_code = final_state.get('generated_code', '') or final_state.get('code', '')

# 检查 1：代码融合度
has_rocm_smi = 'rocm-smi' in final_code
has_stdout_stderr = 'stdout' in final_code and 'stderr' in final_code
has_temperature = 'temperature' in final_code or 'temp' in final_code.lower()

if has_rocm_smi and has_stdout_stderr:
    print('✅ 短期记忆生效！最终代码融合了 rocm-smi + stdout/stderr 捕获')
    if has_temperature:
        print('✅ 且包含 GPU 温度检查')
else:
    print('❌ 代码未融合历史需求')
    print(f'代码片段 ({len(final_code)} chars):\n{final_code[:1000]}...')

# 检查 2：消息历史完整性
all_contents = ' '.join(
    m.get('content', '') if isinstance(m, dict) else str(getattr(m, 'content', m))
    for m in final_state.get('messages', [])
)
if all(k in all_contents for k in ['rocm-smi', 'stdout', 'stderr', 'GPU 温度']):
    print('✅ 消息历史完整保留')
else:
    print('⚠️ 消息历史可能未完整保留')

# 检查 3：各轮代码生成详情
print('\n=== 各轮代码生成详情 ===')
for i, state in enumerate(results, 1):
    code = state.get('generated_code', '') or state.get('code', '')
    validation = state.get('validation_result', {})
    print(f'Round {i}: requirement="{state.get("requirement", "")[:40]}..." '
          f'code_len={len(code)} validation={validation.get("status", "unknown")} '
          f'errors={validation.get("errors", [])}')

print('\n=== 验证长期记忆（Store）===')
for i, state in enumerate(results, 1):
    print(f'Round {i}: requirement="{state.get("requirement", "")[:50]}..."')