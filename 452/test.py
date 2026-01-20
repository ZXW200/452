"""
测试所有智能体代码
Test All Agent Code
"""

print("=" * 60)
print("多智能体博弈系统 - 智能体模块测试")
print("=" * 60)

# ============ 测试1: 导入模块 ============
print("\n【测试1】导入模块...")

try:
    from agent.base_agent import BaseAgent

    print("  ✓ base_agent 导入成功")
except Exception as e:
    print(f"  ✗ base_agent 导入失败: {e}")

try:
    from agent.simple_agent import AlwaysCooperate, AlwaysDefect, RandomAgent

    print("  ✓ simple_agent 导入成功")
except Exception as e:
    print(f"  ✗ simple_agent 导入失败: {e}")

try:
    from agent.med_agent import TitForTat, Pavlov, GrimTrigger

    print("  ✓ med_agent 导入成功")
except Exception as e:
    print(f"  ✗ med_agent 导入失败: {e}")

try:
    from agent.adv_agent import QLearningAgent, FictitiousPlay

    print("  ✓ adv_agent 导入成功")
except Exception as e:
    print(f"  ✗ adv_agent 导入失败: {e}")

try:
    from agent.agent_factory import AgentFactory

    print("  ✓ agent_factory 导入成功")
except Exception as e:
    print(f"  ✗ agent_factory 导入失败: {e}")

# ============ 测试2: 简单策略 ============
print("\n【测试2】简单策略智能体...")

# AlwaysCooperate
allc = AlwaysCooperate(agent_id=0)
print(f"  {allc.strategy_name}: PD行动={allc.choose_action('PD')}, 能力={allc.ability_level}")

# AlwaysDefect
alld = AlwaysDefect(agent_id=1)
print(f"  {alld.strategy_name}: PD行动={alld.choose_action('PD')}, 能力={alld.ability_level}")

# Random
rand = RandomAgent(agent_id=2, coop_probability=0.5)
actions = [rand.choose_action('PD') for _ in range(100)]
coop_rate = actions.count('C') / 100
print(f"  {rand.strategy_name}: 100次中合作率={coop_rate:.2f}, 能力={rand.ability_level}")

# ============ 测试3: 中等策略 ============
print("\n【测试3】中等策略智能体...")

# TitForTat
tft = TitForTat(agent_id=3)
print(f"  {tft.strategy_name} 测试:")
print(f"    第1轮(无历史): {tft.choose_action('PD')}")  # 应该是 C
tft.update('C', 'D', 0)  # 对手背叛
print(f"    第2轮(对手D后): {tft.choose_action('PD')}")  # 应该是 D
tft.update('D', 'C', 5)  # 对手合作
print(f"    第3轮(对手C后): {tft.choose_action('PD')}")  # 应该是 C

# Pavlov
pav = Pavlov(agent_id=4, threshold=2.0)
print(f"  {pav.strategy_name} 测试:")
print(f"    第1轮(无历史): {pav.choose_action('PD')}")  # C
pav.update('C', 'C', 3)  # 赢了(3>=2)
print(f"    第2轮(赢后): {pav.choose_action('PD')}")  # 保持C
pav.update('C', 'D', 0)  # 输了(0<2)
print(f"    第3轮(输后): {pav.choose_action('PD')}")  # 切换到D

# GrimTrigger
grim = GrimTrigger(agent_id=5)
print(f"  {grim.strategy_name} 测试:")
print(f"    初始triggered={grim.triggered}, 行动={grim.choose_action('PD')}")
grim.update('C', 'D', 0)  # 对手背叛！
print(f"    被背叛后triggered={grim.triggered}, 行动={grim.choose_action('PD')}")

# ============ 测试4: 高级策略 ============
print("\n【测试4】高级策略智能体...")

# Q-Learning
q_agent = QLearningAgent(agent_id=6, learning_rate=0.1, epsilon=0.1)
print(f"  {q_agent.strategy_name} 测试:")

# 模拟10轮与始终合作对手的博弈
for i in range(10):
    action = q_agent.choose_action('PD')
    opponent_action = 'C'  # 对手始终合作
    payoff = 3 if action == 'C' else 5  # CC=3, DC=5
    q_agent.update(action, opponent_action, payoff)

print(f"    10轮后Q表: {dict(q_agent.q_table)}")
print(f"    总收益: {q_agent.total_payoff}")

# Fictitious Play
fp = FictitiousPlay(agent_id=7)
print(f"  {fp.strategy_name} 测试:")

# 模拟对手70%合作
import random

random.seed(42)
for i in range(20):
    action = fp.choose_action('PD')
    opponent_action = 'C' if random.random() < 0.7 else 'D'
    payoff = {'CC': 3, 'CD': 0, 'DC': 5, 'DD': 1}[action + opponent_action]
    fp.update(action, opponent_action, payoff)

print(f"    对手行动统计: {dict(fp.opponent_action_counts)}")
total = sum(fp.opponent_action_counts.values())
p_coop = fp.opponent_action_counts['C'] / total if total > 0 else 0
print(f"    估计对手合作概率: {p_coop:.2f}")

# ============ 测试5: 智能体工厂 ============
print("\n【测试5】智能体工厂...")

# 创建单个智能体
agent = AgentFactory.create('TFT', agent_id=100)
print(f"  创建单个: {agent}")

# 创建同质群体
population = AgentFactory.create_population('AllC', n=5)
print(f"  同质群体(AllC×5): {[str(a) for a in population]}")

# 创建混合群体
composition = {'TFT': 2, 'AllD': 2, 'Q-Learn': 1}
mixed = AgentFactory.create_mixed_population(composition)
print(f"  混合群体: {[a.strategy_name for a in mixed]}")

# 打印可用策略
print(f"  可用策略类型: {list(AgentFactory.AGENT_TYPES.keys())}")
print(f"  能力分组: {AgentFactory.ABILITY_GROUPS}")

# ============ 测试6: 模拟一场博弈 ============
print("\n【测试6】模拟TFT vs AllD的10轮博弈...")

# 收益矩阵
PAYOFF = {
    ('C', 'C'): (3, 3),
    ('C', 'D'): (0, 5),
    ('D', 'C'): (5, 0),
    ('D', 'D'): (1, 1)
}

# 创建两个智能体
agent1 = TitForTat(agent_id=0)
agent2 = AlwaysDefect(agent_id=1)

print(f"  {agent1.strategy_name} vs {agent2.strategy_name}")
print(f"  {'轮次':<6} {'A1行动':<8} {'A2行动':<8} {'A1收益':<8} {'A2收益':<8}")
print("  " + "-" * 40)

for round_num in range(1, 11):
    # 选择行动
    action1 = agent1.choose_action('PD')
    action2 = agent2.choose_action('PD')

    # 计算收益
    payoff1, payoff2 = PAYOFF[(action1, action2)]

    # 更新智能体
    agent1.update(action1, action2, payoff1)
    agent2.update(action2, action1, payoff2)

    print(f"  {round_num:<6} {action1:<8} {action2:<8} {payoff1:<8} {payoff2:<8}")

print(f"\n  最终总收益: {agent1.strategy_name}={agent1.total_payoff}, {agent2.strategy_name}={agent2.total_payoff}")

# ============ 完成 ============
print("\n" + "=" * 60)
print("所有测试完成！")
print("=" * 60)
