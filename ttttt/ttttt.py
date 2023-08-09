import requests
import json
import collections
import matplotlib.pyplot as plt

api_key = "ur api key here"
url = 'https://api.start.gg/gql/alpha'

headers = {'Authorization': 'Bearer ' + api_key, 'Content-Type': 'application/json'}

query = """
query TournamentQuery($slug: String, $page: Int!, $perPage: Int!) {
  tournament(slug: $slug) {
    events {
      name
      standings(query: { page: $page, perPage: $perPage }) {
        nodes {
          standing
          entrant {
            name
          }
        }
      }
    }
  }
}
"""

counter = 130
player_counter = collections.Counter()
total_top3 = 0

while counter != 119:
    counter -= 1
    variables = {
      "slug": "onlynoobs" + str(counter),
      "page": 1,
      "perPage": 3
    }
    response = requests.post(url, headers=headers, json={'query': query, 'variables': variables})

    if response.status_code == 200:
        response_json = json.loads(response.text)
        events = response_json['data']['tournament']['events']
        for event in events:
            nodes = event['standings']['nodes']
            for node in nodes:
                entrant_name = node['entrant']['name']
                player_counter[entrant_name] += 1
                total_top3 += 1
    else:
        print(f'Request failed with status code {response.status_code}')

top_players = {player: count for player, count in player_counter.items() if count >= 1}

for player in top_players:
    top_players[player] = (top_players[player] / total_top3) * 100

top_players = dict(sorted(top_players.items(), key=lambda item: item[1], reverse=True))

plt.figure(figsize=(15, 10))
plt.bar(top_players.keys(), top_players.values(), align='edge', width=0.6, color=['grey', 'beige', 'purple', 'green', 'cyan', 'red', 'pink', 'blue', 'yellow', 'lightgreen', 'lightpink', 'orange'])
plt.xlabel('Players')
plt.ylabel('Top 3 Placements')
plt.title('Top 3 appearances in onlynoobs tournaments')
plt.xticks(rotation=65)
plt.show()