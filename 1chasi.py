import pandas as pd
import numpy as np

def input_player_data(num_players):
    player_data = []
    for i in range(num_players):
        print(f"{i+1} 번째 사람의 능력치")
        #스탯 입력 부분
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

def main():
    num_players = int(input("입력할 사람 "))
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

if __name__ == "__main__":
    main()
