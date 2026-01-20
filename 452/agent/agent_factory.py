# 文件：agents/agent_factory.py

from agent.simple_agent import AlwaysCooperate, AlwaysDefect, RandomAgent
from agent.med_agent import TitForTat, Pavlov, GrimTrigger
from agent.adv_agent import QLearningAgent, FictitiousPlay


class AgentFactory:
    """智能体工厂类"""

    AGENT_TYPES = {
        # 低能力
        'AllC': AlwaysCooperate,
        'AllD': AlwaysDefect,
        'Random': RandomAgent,
        # 中等能力
        'TFT': TitForTat,
        'Pavlov': Pavlov,
        'Grim': GrimTrigger,
        # 高能力
        'Q-Learn': QLearningAgent,
        'Fictitious': FictitiousPlay
    }

    ABILITY_GROUPS = {
        'Low': ['AllC', 'AllD', 'Random'],
        'Medium': ['TFT', 'Pavlov', 'Grim'],
        'High': ['Q-Learn', 'Fictitious']
    }

    @classmethod
    def create(cls, agent_type: str, agent_id: int, **kwargs):
        """创建单个智能体"""
        if agent_type not in cls.AGENT_TYPES:
            raise ValueError(f"Unknown agent type: {agent_type}")
        return cls.AGENT_TYPES[agent_type](agent_id, **kwargs)

    @classmethod
    def create_population(cls, agent_type: str, n: int, **kwargs):
        """创建同质群体"""
        return [cls.create(agent_type, i, **kwargs) for i in range(n)]

    @classmethod
    def create_mixed_population(cls, composition: dict, start_id: int = 0):
        """
        创建混合群体
        composition: {'TFT': 10, 'AllD': 5, 'Q-Learn': 5}
        """
        agents = []
        current_id = start_id

        for agent_type, count in composition.items():
            for _ in range(count):
                agents.append(cls.create(agent_type, current_id))
                current_id += 1

        return agents

