# 文件：agents/simple_agents.py

import random
from agent.base_agent import BaseAgent


class AlwaysCooperate(BaseAgent):
    """始终合作 - 最简单的合作策略"""

    def __init__(self, agent_id: int):
        super().__init__(agent_id, memory_length=0)
        self.strategy_name = "AllC"
        self.ability_level = "Low"

    def choose_action(self, game_type: str) -> str:
        if game_type == 'PD':
            return 'C'
        elif game_type == 'COORD':
            return 'A'
        else:  # PG
            return 'C'  # 贡献


class AlwaysDefect(BaseAgent):
    """始终背叛 - 最简单的自私策略"""

    def __init__(self, agent_id: int):
        super().__init__(agent_id, memory_length=0)
        self.strategy_name = "AllD"
        self.ability_level = "Low"

    def choose_action(self, game_type: str) -> str:
        if game_type == 'PD':
            return 'D'
        elif game_type == 'COORD':
            return 'B'
        else:  # PG
            return 'D'  # 不贡献


class RandomAgent(BaseAgent):
    """随机策略"""

    def __init__(self, agent_id: int, coop_probability: float = 0.5):
        super().__init__(agent_id, memory_length=0)
        self.coop_prob = coop_probability
        self.strategy_name = f"Random({coop_probability})"
        self.ability_level = "Low"

    def choose_action(self, game_type: str) -> str:
        if random.random() < self.coop_prob:
            return 'C' if game_type == 'PD' else 'A'
        else:
            return 'D' if game_type == 'PD' else 'B'