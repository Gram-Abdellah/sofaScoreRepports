import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

def fetch_data(api_url):
    response = requests.get(api_url)
    response.raise_for_status()
    return response.json()

def process_team_data(team_id, season_id):
    base_url = 'https://api.sofascore.com/api/v1'
    overview_url = f"{base_url}/team/{team_id}"
    stats_url = f"{base_url}/team/{team_id}/season/{season_id}/statistics"
    tournament_url = f"{base_url}/tournament/{team_id}"

    overview = fetch_data(overview_url)['team']
    stats = fetch_data(stats_url)['statistics']
    tournament = fetch_data(tournament_url)['tournament']

    return {
        'team': overview['name'],
        'tournament': tournament['name'],
        'matches': stats['matches'],
        'wins': stats['wins'],
        'draws': stats['draws'],
        'losses': stats['losses'],
        'goalsScored': stats['goalsScored'],
        'goalsConceded': stats['goalsConceded'],
        'yellowCards': stats['yellowCards'],
        'redCards': stats['redCards']
    }

def create_visualizations(data):
    df = pd.DataFrame(data)
    sns.set(style="whitegrid")

    plt.figure(figsize=(12, 6))
    sns.barplot(x='team', y='goalsScored', data=df, palette='viridis')
    plt.title('Goals Scored by Team')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('reports/goals_scored_by_team.png')

def save_reports(data):
    if not os.path.exists('reports'):
        os.makedirs('reports')

    df = pd.DataFrame(data)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f'reports/team_stats_{timestamp}.csv'
    df.to_csv(csv_filename, index=False)

    create_visualizations(data)
    print(f"Reports saved in 'reports' directory")

if __name__ == "__main__":
    teams = [
        {'team_id': 1, 'season_id': 1},
        {'team_id': 2, 'season_id': 1},
        # Add more teams as needed
    ]

    data = [process_team_data(team['team_id'], team['season_id']) for team in teams]
    save_reports(data)
