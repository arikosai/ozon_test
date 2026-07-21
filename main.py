from hero_find_func import get_tallest_hero


if __name__ == "__main__":
    print("Введите пол (Male/Female) и наличие работы (True/False):")
    gender = input("Пол: ").strip()
    has_work_str = input("Работа: ").strip()

    has_work = has_work_str == "True"

    hero = get_tallest_hero(gender, has_work)
    print()
    print(f"Имя: {hero['name']}")
    print(f"Рост: {hero['appearance']['height'][1]}")
