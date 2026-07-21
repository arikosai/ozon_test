import re
import requests


url = "https://akabab.github.io/superhero-api/api/all.json"


class NoHeroFoundError(Exception):
    pass


def _parse_height_cm(height):
    if not height:
        return None

    for value in height:
        match = re.search(r"([\d.]+)\s*cm", value)
        if match:
            return float(match.group(1))

    return None


def get_tallest_hero(gender, has_work):
    response = requests.get(url)
    heroes = response.json()

    tallest_hero = None
    tallest_height = -1.0

    for hero in heroes:
        appearance = hero.get("appearance", {})
        work = hero.get("work", {})

        hero_gender = appearance.get("gender")
        occupation = work.get("occupation", "-")

        if hero_gender != gender:
            continue

        hero_has_work = occupation not in ("-", "", None)
        if hero_has_work != has_work:
            continue

        height_cm = _parse_height_cm(appearance.get("height"))
        if height_cm is None:
            continue

        if height_cm > tallest_height:
            tallest_height = height_cm
            tallest_hero = hero

    if tallest_hero is None:
        raise NoHeroFoundError(
            f"Не найден герой с полом {gender} и наличием работы {has_work}"
        )

    return tallest_hero
