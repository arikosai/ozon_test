from unittest.mock import patch, MagicMock
import pytest
import requests
from hero_find_func import get_tallest_hero, _parse_height_cm, NoHeroFoundError, url


def make_hero(id, name, gender, height, occupation):
    return {
        "id": id,
        "name": name,
        "appearance": {
            "gender": gender,
            "height": ["irrelevant", height],
        },
        "work": {
            "occupation": occupation,
            "base": "-",
        },
    }


HEROES = [
    make_hero(1, "Alex", "Male", "182 cm", "Musician"),
    make_hero(2, "Misha", "Male", "173 cm", "Chess player"),
    make_hero(3, "Denis", "Male", "190 cm", "-"),
    make_hero(4, "Liza", "Female", "180 cm", "Warrior"),
    make_hero(5, "Eva", "Female", "170 cm", "-"),
    make_hero(6, "Frank", "Male", "220 cm", "-"),
]


def mock_response(json_data):
    response = MagicMock()
    response.json.return_value = json_data
    return response


@patch("hero_find_func.requests.get")
def test_returns_tallest_male_with_work(mock_get):
    mock_get.return_value = mock_response(HEROES)

    hero = get_tallest_hero(gender="Male", has_work=True)

    assert hero["name"] == "Alex"


@patch("hero_find_func.requests.get")
def test_returns_tallest_male_without_work(mock_get):
    mock_get.return_value = mock_response(HEROES)

    hero = get_tallest_hero(gender="Male", has_work=False)

    assert hero["name"] == "Frank"


@patch("hero_find_func.requests.get")
def test_returns_tallest_female_with_work(mock_get):
    mock_get.return_value = mock_response(HEROES)

    hero = get_tallest_hero(gender="Female", has_work=True)

    assert hero["name"] == "Liza"


@patch("hero_find_func.requests.get")
def test_raises_when_no_hero_matches(mock_get):
    mock_get.return_value = mock_response(HEROES)

    with pytest.raises(NoHeroFoundError):
        get_tallest_hero(gender="Nonbinary", has_work=True)


@patch("hero_find_func.requests.get")
def test_hero_with_missing_height_is_ignored(mock_get):
    heroes = [
        make_hero(1, "NoHeight", "Male", "- cm", "Fighter"),
        make_hero(2, "HasHeight", "Male", "175 cm", "Fighter"),
    ]
    mock_get.return_value = mock_response(heroes)

    hero = get_tallest_hero(gender="Male", has_work=True)

    assert hero["name"] == "HasHeight"


@patch("hero_find_func.requests.get")
def test_hero_with_missing_appearance_or_work_field_is_skipped(mock_get):
    heroes = [
        {"id": 1, "name": "Broken"},
        make_hero(2, "Normal", "Male", "180 cm", "Fighter"),
    ]
    mock_get.return_value = mock_response(heroes)

    hero = get_tallest_hero(gender="Male", has_work=True)

    assert hero["name"] == "Normal"


@patch("hero_find_func.requests.get")
def test_empty_heroes_list_raises(mock_get):
    mock_get.return_value = mock_response([])

    with pytest.raises(NoHeroFoundError):
        get_tallest_hero(gender="Male", has_work=True)


def test_parse_height_cm_normal_value():
    assert _parse_height_cm(["6'8", "203 cm"]) == 203.0


def test_parse_height_cm_decimal_value():
    assert _parse_height_cm(["6'8", "203.2 cm"]) == 203.2


def test_parse_height_cm_missing_marker():
    assert _parse_height_cm(["6'8", "- cm"]) is None


def test_parse_height_cm_empty_list():
    assert _parse_height_cm([]) is None


def test_parse_height_cm_none_input():
    assert _parse_height_cm(None) is None


@pytest.mark.api
def test_api_is_accesible():
    response = requests.get(url)

    assert response.status_code == 200


@pytest.mark.api
def test_get_tallest_hero_male_with_work_from_api():
    hero = get_tallest_hero(gender="Male", has_work=True)

    assert hero["appearance"]["gender"] == "Male"
    assert hero["work"]["occupation"] not in ("-", "", None)


@pytest.mark.api
def test_get_tallest_hero_female_without_work_from_api():
    hero = get_tallest_hero(gender="Female", has_work=False)

    assert hero["appearance"]["gender"] == "Female"
    assert hero["work"]["occupation"] in ("-", "", None)
