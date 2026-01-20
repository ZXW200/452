# 文件：agents/base_agent.py

from abc import ABC, abstractmethod
from collections import deque
from typing import List, Tuple, Optional


class BaseAgent(ABC):
    """智能体基类"""

    def __init__(self, agent_id: int, memory_length: int = 10):
        self.id = agent_id
        self.memory = deque(maxlen=memory_length)
        self.total_payoff = 0.0
        self.round_count = 0
        self.strategy_name = "BaseAgent"
        self.ability_level = "Unknown"  # Low / Medium / High

    @abstractmethod
    def choose_action(self, game_type: str) -> str:
        """
        选择行动
        game_type: 'PD', 'COORD', 'PG'
        返回: 行动字符串
        """
        pass

    def update(self, my_action: str, opponent_action: str, payoff: float):
        """更新智能体状态"""
        self.memory.append({
            'my_action': my_action,
            'opponent_action': opponent_action,
            'payoff': payoff,
            'round': self.round_count
        })
        self.total_payoff += payoff
        self.round_count += 1

    def reset(self):
        """重置智能体状态"""
        self.memory.clear()
        self.total_payoff = 0.0
        self.round_count = 0

    def get_last_opponent_action(self) -> Optional[str]:
        """获取对手上一轮的行动"""
        if len(self.memory) > 0:
            return self.memory[-1]['opponent_action']
        return None

    def __repr__(self):
        return f"{self.strategy_name}(id={self.id})"