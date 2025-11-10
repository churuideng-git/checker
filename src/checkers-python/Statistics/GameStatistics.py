class GameStatistics:
    def __init__(self, player, num_games, num_wins, num_draws) -> None:
        self.player = player
        self.num_games = num_games
        self.num_wins = num_wins
        self.num_draws = num_draws

    def __str__(self):
        return (f"Number of games played by {self.player}: {self.num_games} "
                f"| Number of wins: {self.num_wins}")

    def calculate_winrate(self) -> float:
        return self.num_wins / self.num_games * 100

    def calculate_loss(self) -> float:
        return (self.num_games - self.num_wins) / self.num_games * 100

    def calculate_expectation(self) -> float:
        pass

    def get_opponents_stats(self) -> tuple:
        opp_wins = self.num_games - self.num_wins
        opp_draws = self.num_draws
        opp_loss = self.num_wins
        return opp_wins, opp_draws, opp_loss








