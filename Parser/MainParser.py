import requests
import re
from cfg.config import TOKEN


def get_total(game_result):
    yellow_card = {"L": game_result["L"], "01": game_result["O1"], "02": game_result["O2"], "S": game_result["S"], "TOTAL": []}

    # ТОТАЛЫ
    try:
        for idx, all_s in enumerate(game_result["GE"]):
            if all_s["E"][0][0]["T"] == 9:
                for coef_all in all_s["E"]:
                    for coef in coef_all:
                        yellow_card["TOTAL"] += [coef]

        return yellow_card

    except Exception as ex:
        print(ex)


def get_url_match(game_result, champs, game_id):
    champs_name = game_result["LE"]
    champs_name = re.sub(r'[.,é()+]', '', champs_name)
    champs_name = re.sub(r'\s', '-', champs_name)

    command_name_1 = game_result["O1E"]
    command_name_1 = re.sub(r'[.,()+]', '', command_name_1)
    command_name_1 = re.sub(r'\s', '-', command_name_1)

    command_name_2 = game_result["O2E"]
    command_name_2 = re.sub(r'[.,()+]', '', command_name_2)
    command_name_2 = re.sub(r'\s', '-', command_name_2)

    url = "https://1xstavka.ru/live/football/" + f"{champs}" + f"-{champs_name}/" + f"{game_id}" + f"-{command_name_1}-{command_name_2}"
    return url


def get_game(result, message, what):
    text = f"Информация о Live матчах\n{what}\n\n"
    idx = 0
    for game in result["Value"]:
        game_id = game["I"]
        champs = game["LI"]
        params = (
            ("id", game_id),
            ("lng", "ru"),
            ("cfview", "0"),
            ("isSubGames", "true"),
            ("GroupEvents", "true"),
            ("allEventsGroupSubGames", "true"),
            ("countevents", "250"),
            ("partner", "51"),
            ("grMode", "2"),
            ("marketType", "1"),
            ("isNewBuilder", "true"),
        )
        response = requests.get("https://1xstavka.ru/LiveFeed/GetGameZip", params=params).json()

        try:
            try:
                try:
                    score_match = f'{response["Value"]["SC"]["FS"]["S1"]}' + ":" + f'{response["Value"]["SC"]["FS"]["S2"]}'
                except:
                    score_match = '0' + ":" + f'{response["Value"]["SC"]["FS"]["S2"]}'
            except:
                score_match = f'{response["Value"]["SC"]["FS"]["S1"]}' + ":" + '0'
        except:
            score_match = "0:0"

        if what == "Тотал жёлтых":
            try:
                for yellow_c in response["Value"]["SG"]:
                    try:
                        if yellow_c["TG"] == "Желтые карточки":
                            try:
                                yellow_c["PN"]
                            except:
                                game_id_2 = yellow_c["I"]
                                params = (
                                    ("id", game_id_2),

                                    ("lng", "ru"),
                                    ("cfview", "0"),
                                    ("isSubGames", "true"),
                                    ("GroupEvents", "true"),
                                    ("allEventsGroupSubGames", "true"),
                                    ("countevents", "250"),
                                    ("partner", "51"),
                                    ("grMode", "2"),
                                    ("marketType", "1"),
                                    ("isNewBuilder", "true"),
                                )
                                response = requests.get("https://1xstavka.ru/LiveFeed/GetGameZip", params=params).json()
                                try:
                                    try:
                                        try:
                                            score_match = f'{response["Value"]["SC"]["FS"]["S1"]}' + ":" + f'{response["Value"]["SC"]["FS"]["S2"]}'
                                        except:
                                            score_match = '0' + ":" + f'{response["Value"]["SC"]["FS"]["S2"]}'
                                    except:
                                        score_match = f'{response["Value"]["SC"]["FS"]["S1"]}' + ":" + '0'
                                except:
                                    score_match = "0:0"

                                url = get_url_match(response["Value"], champs, game_id_2)
                                total_all = get_total(response["Value"])
                                count_total = int(len(total_all["TOTAL"]) / 2)
                                i_koef = count_total

                                i = 0
                                total_match = int(score_match[0]) + int(score_match[-1])
                                if int(total_match) == int(message.text):
                                    text += f"{idx + 1}. {url}\n\n  Тотал жёлтых: {total_match}\n  Счёт жёлт карт: {score_match}\n  Команды: {total_all['01']} : {total_all['02']}\n\n  Коэфы на тоталы\n"
                                    while i < count_total:
                                        text += f'    {total_all["TOTAL"][int(i)]["P"]} Б/М:   {total_all["TOTAL"][i]["C"]} / {total_all["TOTAL"][i_koef]["C"]}\n'

                                        i += 1
                                        i_koef += 1
                                    text += f"\n" + "➖" * 10 + "\n\n"
                    except:
                        ...
            except:
                ...

        else:
            url = get_url_match(response["Value"], champs, game_id)
            total_all = get_total(response["Value"])
            count_total = int(len(total_all["TOTAL"]) / 2)
            i_koef = count_total

            i = 0
            total_match = int(score_match[0]) + int(score_match[-1])
            if int(total_match) == int(message.text):
                text += f"{idx + 1}. {url}\n\n  Счёт: {score_match}\n  Команды: {total_all['01']} : {total_all['02']}\n\n  Коэфы на тоталы\n"
                while i < count_total:
                    text += f'    {total_all["TOTAL"][int(i)]["P"]} Б/М:   {total_all["TOTAL"][i]["C"]} / {total_all["TOTAL"][i_koef]["C"]}\n'
                    i += 1
                    i_koef += 1
                text += f"\n" + "➖" * 10 + "\n\n"

        if idx == 9:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={message.from_user.id}&text={text}")
            text = f"Информация о Live матчах\n{what}\n\n"
            idx = 0
        idx += 1
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={message.from_user.id}&text={text}")


async def start_pars(message, count, what):
    params = (
        ("sports", "1"),
        ("count", count),
        ("antisports", "188"),
        ("mode", "4"),
        ("country", "1"),
        ("partner", "51"),
        ("getEmpty", "true"),

        ("noFilterBlockEvent", "true")
    )

    response = requests.get("https://1xstavka.ru/LiveFeed/Get1x2_VZip", params=params).json()
    get_game(response, message, what)
