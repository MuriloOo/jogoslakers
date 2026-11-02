"""Consulta pública do calendário dos Lakers na ESPN, sem dependências externas."""

import argparse
import json
import sys
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


URL = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams/lal/schedule"


def normalize(payload):
    games = []
    for event in payload.get("events", []):
        competition = event["competitions"][0]
        teams = {}
        for team in competition["competitors"]:
            score = team.get("score")
            if isinstance(score, dict):
                score = score.get("value")
            teams[team["homeAway"]] = {
                "nome": team["team"]["displayName"],
                "pontos": score,
            }
        games.append({
            "id": event["id"],
            "data_utc": event["date"],
            "status": competition.get("status", event.get("status", {})).get("type", {}).get("description", "Desconhecido"),
            "casa": teams["home"],
            "visitante": teams["away"],
        })
    return sorted(games, key=lambda game: game["data_utc"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--season", type=int, help="Ano final da temporada; por exemplo, 2026 para 2025–26")
    parser.add_argument("--seasontype", type=int, choices=(1, 2, 3), default=2,
                        help="1: pré-temporada; 2: temporada regular (padrão); 3: playoffs")
    args = parser.parse_args()
    url = URL + f"?seasontype={args.seasontype}"
    if args.season:
        url += f"&season={args.season}"
    try:
        with urlopen(url, timeout=30) as response:
            games = normalize(json.load(response))
    except (HTTPError, URLError, TimeoutError, OSError, ValueError, KeyError, IndexError, TypeError) as error:
        print(f"Não foi possível consultar os Lakers: {error}", file=sys.stderr)
        return 1
    print(json.dumps(games, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
