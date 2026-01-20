# 文件：agents/advanced_agents.py

import random
from collections import defaultdict
from agent.base_agent import BaseAgent


class QLearningAgent(BaseAgent):
    """
    Q-Learning智能体
    通过强化学习适应对手策略
    """

    def __init__(self, agent_id: int, learning_rate: float = 0.1,
                 discount_factor: float = 0.95, epsilon: float = 0.1):
        super().__init__(agent_id, memory_length=50)
        self.alpha = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon
        self.strategy_name = "Q-Learn"
        self.ability_level = "High"

        # Q表：state -> action -> value
        # 状态简化为对手上一轮的行动
        self.q_table = defaultdict(lambda: defaultdict(float))

    def _get_state(self) -> str:
        """获取当前状态"""
        last_opponent = self.get_last_opponent_action()
        return last_opponent if last_opponent else 'init'

    def choose_action(self, game_type: str) -> str:
        state = self._get_state()
        actions = ['C', 'D'] if game_type == 'PD' else ['A', 'B']

        # ε-greedy策略
        if random.random() < self.epsilon:
            return random.choice(actions)

        # 选择Q值最高的行动
        q_values = {a: self.q_table[state][a] for a in actions}
        max_q = max(q_values.values())
        best_actions = [a for a, q in q_values.items() if q == max_q]

        return random.choice(best_actions)

    def update(self, my_action: str, opponent_action: str, payoff: float):
        old_state = self._get_state()

        # 调用父类更新
        super().update(my_action, opponent_action, payoff)

        new_state = opponent_action

        # Q-Learning更新公式
        old_q = self.q_table[old_state][my_action]
        max_next_q = max(self.q_table[new_state].values()) if self.q_table[new_state] else 0

        new_q = old_q + self.alpha * (payoff + self.gamma * max_next_q - old_q)
        self.q_table[old_state][my_action] = new_q

    def reset(self):
        super().reset()
        # 保留Q表（迁移学习）或清空
        # self.q_table.clear()  # 取消注释则完全重置


class FictitiousPlay(BaseAgent):
    """
    虚拟博弈策略
    根据对手历史行为的频率预测，选择最优响应
    """

    def __init__(self, agent_id: int):
        super().__init__(agent_id, memory_length=100)
        self.opponent_action_counts = defaultdict(int)
        self.strategy_name = "Fictitious"
        self.ability_level = "High"

    def _get_opponent_probability(self, action: str) -> float:
        """估计对手选择某行动的概率"""
        total = sum(self.opponent_action_counts.values())
        if total == 0:
            return 0.5
        return self.opponent_action_counts[action] / total

    def choose_action(self, game_type: str) -> str:
        if sum(self.opponent_action_counts.values()) < 2:
            # 历史太少，先合作
            return 'C' if game_type == 'PD' else 'A'

        if game_type == 'PD':
            # 计算期望收益
            p_coop = self._get_opponent_probability('C')

            # E[C] = 3*p(C) + 0*p(D) = 3*p_coop
            # E[D] = 5*p(C) + 1*p(D) = 5*p_coop + (1-p_coop)
            e_cooperate = 3 * p_coop + 0 * (1 - p_coop)
            e_defect = 5 * p_coop + 1 * (1 - p_coop)

            return 'C' if e_cooperate >= e_defect else 'D'

        else:  # COORD
            p_a = self._get_opponent_probability('A')

            # E[A] = 4*p(A) + 0*p(B)
            # E[B] = 0*p(A) + 2*p(B)
            e_a = 4 * p_a
            e_b = 2 * (1 - p_a)

            return 'A' if e_a >= e_b else 'B'

    def update(self, my_action: str, opponent_action: str, payoff: float):
        super().update(my_action, opponent_action, payoff)
        self.opponent_action_counts[opponent_action] += 1

    def reset(self):
        super().reset()
        self.opponent_action_counts.clear()