# 文件：agents/medium_agents.py

from agent.base_agent import BaseAgent


class TitForTat(BaseAgent):
    """
    以牙还牙策略
    - 第一轮合作
    - 之后复制对手上一轮的行动
    """

    def __init__(self, agent_id: int):
        super().__init__(agent_id, memory_length=1)
        self.strategy_name = "TFT"
        self.ability_level = "Medium"

    def choose_action(self, game_type: str) -> str:
        last_opponent = self.get_last_opponent_action()

        if last_opponent is None:
            # 第一轮：合作
            return 'C' if game_type == 'PD' else 'A'

        # 复制对手上一轮行动
        return last_opponent


class Pavlov(BaseAgent):
    """
    Win-Stay, Lose-Shift 策略
    - 如果上一轮收益好，重复行动
    - 如果上一轮收益差，改变行动
    """

    def __init__(self, agent_id: int, threshold: float = 2.0):
        super().__init__(agent_id, memory_length=1)
        self.threshold = threshold
        self.strategy_name = "Pavlov"
        self.ability_level = "Medium"
        self.last_action = None

    def choose_action(self, game_type: str) -> str:
        if len(self.memory) == 0:
            self.last_action = 'C' if game_type == 'PD' else 'A'
            return self.last_action

        last_payoff = self.memory[-1]['payoff']

        if last_payoff >= self.threshold:
            # Win-Stay: 保持上一轮行动
            return self.last_action
        else:
            # Lose-Shift: 改变行动
            if game_type == 'PD':
                self.last_action = 'D' if self.last_action == 'C' else 'C'
            else:
                self.last_action = 'B' if self.last_action == 'A' else 'A'
            return self.last_action

    def update(self, my_action: str, opponent_action: str, payoff: float):
        super().update(my_action, opponent_action, payoff)
        self.last_action = my_action


class GrimTrigger(BaseAgent):
    """
    冷酷触发策略
    - 开始时合作
    - 一旦对手背叛，永远背叛
    """

    def __init__(self, agent_id: int):
        super().__init__(agent_id, memory_length=100)
        self.triggered = False
        self.strategy_name = "Grim"
        self.ability_level = "Medium"

    def choose_action(self, game_type: str) -> str:
        if self.triggered:
            return 'D' if game_type == 'PD' else 'B'
        return 'C' if game_type == 'PD' else 'A'

    def update(self, my_action: str, opponent_action: str, payoff: float):
        super().update(my_action, opponent_action, payoff)
        # 检测背叛
        if opponent_action in ['D', 'B']:
            self.triggered = True

    def reset(self):
        super().reset()
        self.triggered = False