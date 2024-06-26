import json
from jinja2 import Template
import pdfkit
import os
import requests

def generate_html_report(data):
    with open('template.html', 'r') as f:
        template_content = f.read()

    template = Template(template_content)
    for club_data in data:
        club_info = club_data[0][0]
        club_name = club_info['team']
        tournament = club_info['tournament']
        
        html_out = template.render(club_data=club_data)
        
        html_filename = f"rapports/html/{tournament}/{club_name.replace(' ', '_')}_Season_Report.html"
        pdf_filename = f"rapports/pdf/{tournament}/{club_name.replace(' ', '_')}_Season_Report.pdf"
        
        if not os.path.exists(f"rapports/html/{tournament}"):
            os.makedirs(f"rapports/html/{tournament}")
            
        if not os.path.exists(f"rapports/pdf/{tournament}"):
            os.makedirs(f"rapports/pdf/{tournament}")
        
        with open(html_filename, 'w') as f:
            f.write(html_out)
        
        try:
            pdfkit.from_file(html_filename, pdf_filename, options=None)
            print(f"Generated {pdf_filename}")
        except Exception as e:
            print(f"Error generating {pdf_filename}: {e}")

def get_data(base_url, endpoint):
    url = f"{base_url}/{endpoint}"
    response = requests.get(url)
    response.raise_for_status()  # Ensure we notice bad responses
    return response.json()

def createRapport(team_id, season_id, tournament_id):
    base_url = 'https://api.sofascore.com/api/v1'
    
    # Team overview
    overview = get_data(base_url, f'team/{team_id}').get('team', {})
    
    # Team statistics
    stats = get_data(base_url, f'team/{team_id}/season/{season_id}/statistics').get('statistics', {})
    
    # Tournament info
    tournament = get_data(base_url, f'tournament/{tournament_id}').get('tournament', {})
    
    statistical_analysis = {
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

    data = [[overview, stats, statistical_analysis]]
    return data


def get_data(link , api_link):
    headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,fr;q=0.8',
    'cache-control': 'max-age=0',
    'priority': 'u=1, i',
    'referer': link,
    'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'x-requested-with': 'a9a757',
    } 
    response = requests.get(
        'https://www.sofascore.com/api/v1/'+ api_link,
        headers=headers,
    )
    time.sleep(1) 
    return response
    
    clubs_sorted = sorted(clubs, key=lambda x: x['position'])
    index = next((i for i, club in enumerate(clubs_sorted) if club['team']['id'] == team_id), None)
    
    if index is None:
        return None
    
    indices = [index]
    for i in range(1, 3):
        if index - i >= 0:
            indices.append(index - i)
    for i in range(1, 3):
        if index + i < len(clubs_sorted):
            indices.append(index + i)
    
    return [clubs_sorted[i] for i in sorted(indices)]

# Main script
if __name__ == "__main__":
    base_url = 'https://api.sofascore.com/api/v1'
    
    rows = get_data(base_url, 'tournament/1/season/52186/standings/total').get('standings', [])[0]['rows']
    IDs = [{'id': row['team']['id']} for row in rows]
    
    for team_id in IDs:
        try:
            generate_html_report([createRapport(team_id['id'], 1, 17)])
        except Exception as e:
            print(f"Error processing team {team_id['id']}: {e}")
