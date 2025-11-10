from GameLogic import GameLogic
from StudentAI import StudentAI
from AI_Extensions.RandomAI import StudentAI as AI
from Statistics.GameStatistics import GameStatistics

def get_player_turns(player, opponent, match_no, alternate_starts=True) -> tuple:
    if match_no % 2 == 1 and alternate_starts:
        return opponent, player
    else:
        return player, opponent

class GameSimulation:

    def __init__(self, player, opponent, game_logic=GameLogic):
        self.player = player
        self.opponent = opponent
        self.game_logic = game_logic  # default to GameLogic

    def simulate(self, col, row, p, num_games, alternate_starts=True, quiet=True) -> dict:

        results = {"num_games": num_games, "p1_wins": 0, "p2_wins": 0, "ties": 0}

        for i in range(num_games):
            first_player, second_player = get_player_turns(
                self.player, self.opponent, match_no=i, alternate_starts=alternate_starts
            )

            ai1 = first_player(col, row, p)
            ai2 = second_player(col, row, p)

            game = self.game_logic(col, row, p, mode="local", debug=not quiet)
            game.ai_list = [ai1, ai2]
            winner = game.gameloop(fh=None)

            if alternate_starts and i % 2 == 1:
                if winner == 1:
                    results["p2_wins"] += 1
                elif winner == 2:
                    results["p1_wins"] += 1
                else:
                    results["ties"] += 1
            else:
                if winner == 1:
                    results["p1_wins"] += 1
                elif winner == 2:
                    results["p2_wins"] += 1
                else:
                    results["ties"] += 1

        return results


if __name__=="__main__":
    simulation = GameSimulation(StudentAI, AI)
    results = simulation.simulate(col=8, row=8, p=3, num_games=10, alternate_starts=True, quiet=True)

    p1_stats = GameStatistics(
        player="Player 1",
        num_games=results["num_games"],
        num_wins=results["p1_wins"],
        num_draws=results["ties"],
    )
    p2_stats = GameStatistics(
        player="Player 2",
        num_games=results["num_games"],
        num_wins=results["p2_wins"],
        num_draws=results["ties"],
    )

    total = results["num_games"]
    draws = results["ties"]
    p1_losses = results["p2_wins"]
    p2_losses = results["p1_wins"]

    print("\n==== Simulation Results ====")
    print(f"Games: {total}")
    print(f"Draws: {draws}")
    print(f"\nPlayer 1: {simulation.player}")
    print(f"- Wins:   {p1_stats.num_wins}")
    print(f"- Losses: {p1_losses}")
    print(f"- Draws:  {p1_stats.num_draws}")
    print(f"- Winrate: {p1_stats.calculate_winrate():.1f}% | Loss rate: {p1_stats.calculate_loss():.1f}%")

    print(f"\nPlayer 2: {simulation.opponent}")
    print(f"- Wins:   {p2_stats.num_wins}")
    print(f"- Losses: {p2_losses}")
    print(f"- Draws:  {p2_stats.num_draws}")
    print(f"- Winrate: {p2_stats.calculate_winrate():.1f}% | Loss rate: {p2_stats.calculate_loss():.1f}%")
