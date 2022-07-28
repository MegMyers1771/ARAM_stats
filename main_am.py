import ChampsID2
import os.path
import time
import requests

regions = ['la1', 'la2', 'br1', 'na1']

with open('api.txt', 'r', encoding="utf-8") as file:
    api_k = file.readline()


def parse_to_txt(t1, t2, kills, w_check, id_):

    with open ('Stats_AM.txt', 'a+') as stats_file:
        if w_check:
            stats_file.writelines(f"[W1]-|-{t1}__{t2}-|-{kills}-|-{id_}\n")
        else:
            stats_file.writelines(f"[W2]-|-{t1}__{t2}-|-{kills}-|-{id_}\n")
            pass
            
        stats_file.close()


def getting_gamelists(reg_, names_collection):
    puuid_list = []
    counts = 0
    for pd in names_collection:
        try:
            response = requests.get(
                f"https://{reg_}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{pd}?api_key={api_k}"
            ).json()
            # os.system('cls')
            puuid_list.append(response['puuid'])
            os.system('cls')
            print(f"Done [{counts}]")
            counts += 1
        except KeyError:
            print('Cooldown 120')
            time.sleep(120)
            continue
        except requests.ConnectionError:
            print('Request connection error. Connection aborted. Reconection after 20 second')
            time.sleep(20)
            continue

    all_games_list = []
    x = 0
    for items in puuid_list:
        try:
            response = requests.get(
                f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{items}/ids?start=0&count=20&api_key={api_k}"
            ).json()
            for match in range(0, len(response)):
                all_games_list.append(response[match])
            os.system('cls')
            print(f"{x} - collected")
            x += 1
        except KeyError:
            print('Cooldown 120')
            time.sleep(120)
            continue
        except requests.ConnectionError:
            print('Request connection error. Connection aborted. Reconection after 20 second')
            time.sleep(20)
            continue

    all_games_list = set(all_games_list)

    for match_ in all_games_list:

        try:

            response = requests.get(
                f"https://americas.api.riotgames.com/lol/match/v5/matches/{match_}?api_key={api_k}"
            ).json()
            os.system('cls')

            if response['info']['gameMode'] == "ARAM":
                match_dict = dict.fromkeys(['team_1_champs', 'team_2_champs'])
                match_dict['team_1_champs'] = []
                match_dict['team_2_champs'] = []
                t1_kills = 0
                t2_kills = 0
                for champ_1 in range(0, 5):
                    role_parse = str(response['info']['participants'][champ_1]['championName'].strip())
                    match_dict['team_1_champs'].append(ChampsID2.converting(role_parse))

                match_dict['team_1_champs'] = sorted(match_dict['team_1_champs'])
                match_dict['team_1_champs'] = ' - '.join([str(item) for item in match_dict['team_1_champs']])

                for champ_2 in range(5, 10):
                    role_parse = str(response['info']['participants'][champ_2]['championName'].strip())
                    match_dict['team_2_champs'].append(ChampsID2.converting(role_parse))

                match_dict['team_2_champs'] = sorted(match_dict['team_2_champs'])
                match_dict['team_2_champs'] = ' - '.join([str(item) for item in match_dict['team_2_champs']])

                kills = 0

                for k in range(0, 10):
                    kills += response['info']['participants'][k]['kills']

                parse_to_txt(match_dict['team_1_champs'],
                             match_dict['team_2_champs'],
                             kills,
                             response['info']['teams'][0]['win'],
                             match_)

                print(f"Game {match_} collected")
                time.sleep(1.5)

            else:
                continue
        except KeyError:
            print("Request error: cooldown 120 sec")
            time.sleep(120)
            continue
        except IndexError:
            continue
        except requests.ConnectionError:
            print('Request connection error. Connection aborted. Reconection after 20 second')
            time.sleep(20)
            continue


def getting_summoners(reg_, names_collection):
    try:

        response = requests.get(
            f"https://{reg_}.api.riotgames.com/lol/spectator/v4/featured-games?api_key={api_k}"
        ).json()

        for s in range(0, len(response['gameList'])):
            if response['gameList'][s]['platformId'] == reg_.upper():
                for v in range(0, 10):
                    names_collection.append(
                        (response['gameList'][s]['participants'][v]['summonerName']).strip()
                    )
            else:
                continue
    except IndexError:
        pass
    except requests.ConnectionError:
        print('Request connection error. Connection aborted. Reconection after 20 second')
        time.sleep(20)
        getting_summoners(reg_, names_collection)

    set(names_collection)
    print("Names collected")

    return names_collection


def main():
    while True:

        for reg_ in regions:
            print(reg_)
            names_collection = []
            getting_summoners(reg_, names_collection)
            getting_gamelists(reg_, names_collection)


if __name__ == "__main__":
    main()


