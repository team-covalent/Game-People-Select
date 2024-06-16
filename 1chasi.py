import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def input_player_data(num_players):
    player_data = []
    for i in range(num_players):
        print(f"{i+1} 번째 사람의 능력치")
        level = int(input("게임레벨: "))
        attack = int(input("공격력: "))
        defense = int(input("방어력: "))
        player_data.append({"Player": i+1, "Level": level, "Attack": attack, "Defense": defense})
    return pd.DataFrame(player_data)

def allocate_teams(df, num_teams, criteria):
    df["Team"] = np.nan
    sorted_df = df.sort_values(by=criteria, ascending=False).reset_index(drop=True)
    
    for i in range(len(sorted_df)):
        sorted_df.at[i, "Team"] = (i % num_teams) + 1

    return sorted_df

def print_teams(df, num_teams):
    teams = {i: [] for i in range(1, num_teams+1)}
    for idx, row in df.iterrows():
        teams[int(row["Team"])].append(row["Player"])

    for team, members in teams.items():
        print(f"팀 {team}: {', '.join(map(str, members))}")

def plot_teams(df, criteria):
    colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k']
    teams = df['Team'].unique()
    
    for team in teams:
        team_data = df[df['Team'] == team]
        x = team_data['Player']
        y = team_data[criteria]
        plt.scatter(x, y, label=f'Team {int(team)}', color=colors[int(team) % len(colors)])
    
    plt.xlabel('Player Number')
    plt.ylabel('Value')
    plt.title(f'Player Stats by Team ({criteria})')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    num_players = int(input("입력할 사람: "))
    player_df = input_player_data(num_players)
    
    num_teams = int(input("팀 인원: "))
    criteria = input("팀나누는 기준 (average or std_dev): ").strip().lower()
    
    if criteria == "average":
        sorted_criteria = ["Level", "Attack", "Defense"]
    elif criteria == "std_dev":
        sorted_criteria = ["Level", "Attack", "Defense"]
    else:
        print("유효하지않는 입력, 평균으로 설정합니다.")
        sorted_criteria = ["Level", "Attack", "Defense"]
    
    teams_df = allocate_teams(player_df, num_teams, sorted_criteria)
    print_teams(teams_df, num_teams)
    
    if criteria == "average":
        plot_teams(teams_df, 'Level')
        plot_teams(teams_df, 'Attack')
        plot_teams(teams_df, 'Defense')
    elif criteria == "std_dev":
        player_df['Level_std'] = (player_df['Level'] - player_df['Level'].mean()) / player_df['Level'].std()
        player_df['Attack_std'] = (player_df['Attack'] - player_df['Attack'].mean()) / player_df['Attack'].std()
        player_df['Defense_std'] = (player_df['Defense'] - player_df['Defense'].mean()) / player_df['Defense'].std()
        teams_df = allocate_teams(player_df, num_teams, ['Level_std', 'Attack_std', 'Defense_std'])
        plot_teams(teams_df, 'Level_std')
        plot_teams(teams_df, 'Attack_std')
        plot_teams(teams_df, 'Defense_std')

if __name__ == "__main__":
    main()
