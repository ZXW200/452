# 文件：games/base_games.py

"""
三类博弈的基础实现
"""


class PrisonersDilemma:
    """囚徒困境"""

    # 收益矩阵: (我的收益, 对手收益)
    PAYOFF_MATRIX = {
        ('C', 'C'): (3, 3),  # R: 双方合作的奖励
        ('C', 'D'): (0, 5),  # S: 被背叛的损失, T: 背叛的诱惑
        ('D', 'C'): (5, 0),  # T, S
        ('D', 'D'): (1, 1)  # P: 双方背叛的惩罚
    }

    def __init__(self, R=3, S=0, T=5, P=1):
        """可自定义收益参数"""
        # 验证囚徒困境条件: T > R > P > S
        assert T > R > P > S, "不满足囚徒困境条件"
        self.PAYOFF_MATRIX = {
            ('C', 'C'): (R, R),
            ('C', 'D'): (S, T),
            ('D', 'C'): (T, S),
            ('D', 'D'): (P, P)
        }

    def play(self, action1: str, action2: str) -> tuple:
        """
        执行一次博弈
        返回: (玩家1收益, 玩家2收益)
        """
        return self.PAYOFF_MATRIX[(action1, action2)]

    def get_actions(self) -> list:
        return ['C', 'D']


class CoordinationGame:
    """协调博弈 - 存在多个纳什均衡"""

    def __init__(self, high_payoff=4, low_payoff=2, mismatch=0):
        self.PAYOFF_MATRIX = {
            ('A', 'A'): (high_payoff, high_payoff),  # 高收益均衡
            ('A', 'B'): (mismatch, mismatch),
            ('B', 'A'): (mismatch, mismatch),
            ('B', 'B'): (low_payoff, low_payoff)  # 低收益均衡
        }

    def play(self, action1: str, action2: str) -> tuple:
        return self.PAYOFF_MATRIX[(action1, action2)]

    def get_actions(self) -> list:
        return ['A', 'B']


class PublicGoodsGame:
    """公共品博弈 - N人博弈"""

    def __init__(self, n_players: int, multiplier: float = 1.5,
                 endowment: float = 10.0):
        """
        n_players: 玩家数量
        multiplier: 公共品乘数 (通常 1 < r < n)
        endowment: 每人初始资源
        """
        self.n = n_players
        self.r = multiplier
        self.endowment = endowment

    def play(self, contributions: list) -> list:
        """
        contributions: 每个玩家的贡献列表 [c1, c2, ..., cn]
        返回: 每个玩家的最终收益列表
        """
        assert len(contributions) == self.n

        total_contribution = sum(contributions)
        public_benefit = self.r * total_contribution / self.n

        payoffs = []
        for c in contributions:
            # 收益 = 保留的资源 + 公共品收益
            payoff = (self.endowment - c) + public_benefit
            payoffs.append(payoff)

        return payoffs

    def get_actions(self) -> list:
        """简化为二元选择：贡献全部或不贡献"""
        return [0, self.endowment]


# ============ 测试代码 ============
if __name__ == "__main__":
    # 测试囚徒困境
    pd = PrisonersDilemma()
    assert pd.play('C', 'C') == (3, 3)
    assert pd.play('C', 'D') == (0, 5)
    print("✓ 囚徒困境测试通过")

    # 测试协调博弈
    cg = CoordinationGame()
    assert cg.play('A', 'A') == (4, 4)
    assert cg.play('A', 'B') == (0, 0)
    print("✓ 协调博弈测试通过")

    # 测试公共品博弈
    pg = PublicGoodsGame(n_players=4, multiplier=2.0, endowment=10)
    payoffs = pg.play([10, 10, 0, 0])  # 两人贡献，两人搭便车
    print(f"公共品收益: {payoffs}")
    # 贡献者: 0 + (2*20/4) = 10
    # 搭便车: 10 + (2*20/4) = 20
    print("✓ 公共品博弈测试通过")