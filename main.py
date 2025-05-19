import random, os, json

UPPER_VOWEL = "АЕЁИОУЫЭЮЯ"
VOWEL = "аеёиоуыэюя"

filename_words = 'words.txt'
filename_statistic = 'statistic.json'

show_counter = True # показывать нумерацию слов в тренировке


class App:
    def __init__(self):
        self.active_test = True

        try:
            with open(filename_statistic, 'r', encoding='utf-8') as file:
                self.statistic_data = json.loads(file.read())
        except:
            self.statistic_data = {
                "training_count": 0,
                "word_count": 0,
                "right_word_count": 0,
                "heavy_words": {}
            }
            with open(filename_statistic, 'w', encoding='utf-8') as file:
                file.write(json.dumps(self.statistic_data, ensure_ascii=False, indent=4))

        if os.path.exists(filename_words):
            with open(filename_words, 'r', encoding='utf-8') as file:
                self.words = [line.strip() for line in file]
        else:
            print(f"Файл {filename_words} не найден")
            self.exit(1)

        if not self.is_format(self.words):
            print(f"В файле {filename_words} ошибка. Для остальной информации введите '0' для помощи")
            self.active_test = False

        self.current_word_count = 0
        self.current_right_word_count = 0

    def start(self):
        while True:
            if not self.active_test:
                answer = None
                while answer not in [0, 1, 2, 3]:
                    print("\nМЕНЮ")
                    print(" ├0── помощь")
                    print(" ├1── тренировка")
                    print(" ├2── статистика")
                    print(" └3── выход")
                    try:answer = int(input(">> "))
                    except: pass
                if answer == 0:
                    self.help()
                elif answer == 1:
                    self.active_test = True
                elif answer == 2:
                    self.statistic()
                elif answer == 3:
                    self.exit(0)
            else:
                self.training_word()

    def training_word(self):
        word = random.choice(self.words)
        word_lower = word.lower()
        vowel_index = self.get_vowel_index(word_lower)

        options_str = ""
        for i, vowel in enumerate(vowel_index):
            options_str += " " * (vowel[0] - len(options_str))
            options_str += str(i + 1)

        answer =  None
        while answer is None or not (0 < answer <= len(vowel_index)):
            if show_counter:
                print(f"\n({self.current_right_word_count}/{self.current_word_count})\n{word_lower}")
            else:
                print("\n" + word_lower)
            print(options_str)
            try: answer = int(input(">> "))
            except: pass

        self.statistic_data["word_count"] += 1
        self.current_word_count += 1
        if not word[vowel_index[answer-1][0]].islower():
            self.statistic_data["right_word_count"] += 1
            self.current_right_word_count += 1
            print("Правильно!")
        else:
            input(f"Неправильно! Правильный ответ: {word}")
            self.statistic_data["training_count"] += 1
            if word in self.statistic_data["heavy_words"]:
                self.statistic_data["heavy_words"][word] += 1
            else:
                self.statistic_data["heavy_words"][word] = 1
            self.active_test = 0

    def help(self):
        print("\nОписание:")
        print(" Программа AccentEGE. Навигация производится по подсказкам.")
        input("[нажмите Enter]")
        print("\nИнформация:")
        print(f" {filename_words} - файл со всеми словами и ударениями; каждая строка файла - отдельное слово, ударение выделяется большой буквой.")
        input("[нажмите Enter]")
        print("\nРекомендации:")
        print(f" 1. Не использовать нескольких заглавных букв в слове внутри файла {filename_words}")
        print(f" 2. Не оставлять пустым файл {filename_words}")
        print(" 3. Не завершать работу программы комбинацией CTRL + Z или CTRL + С")
        input("[нажмите Enter]")

    def statistic(self):
        training_count = self.statistic_data["training_count"]
        word_count = self.statistic_data["word_count"]
        procent = round((self.statistic_data["right_word_count"] / self.statistic_data["word_count"]) * 100, 1)
        erroneous_word = None
        erroneous_count = 0
        for word, count in self.statistic_data["heavy_words"].items():
            if count > erroneous_count:
                erroneous_word = word
                erroneous_count = count

        print("\nСтатистика:")
        print(" - Количество тренировок: ", training_count)
        print(" - Количество слов: ", word_count)
        print(" - Правильных: ", procent, "%")
        print(" - Наибольшее число ошибок в слове: ", erroneous_word)
        input("[нажмите Enter]")

        self.current_right_word_count = 0
        self.current_word_count = 0

        self.save_statistic()

    def exit(self, code=0):
        self.save_statistic()
        exit(code)

    def save_statistic(self):
        with open(filename_statistic, "w", encoding="utf-8") as file:
            file.write(json.dumps(self.statistic_data, ensure_ascii=False, indent=4))

    def get_vowel_index(self, word):
        ind_vowal = []
        for i, ltr in enumerate(word):
            if ltr == " ":
                break
            if ltr in VOWEL:
                ind_vowal.append((i, ltr))
        return ind_vowal

    def is_format(self, words):
        flag = True
        for word in words:
            if sum(int(ltr in UPPER_VOWEL) for ltr in word) != 1:
                print(word)
                flag = False
                break
        return (flag and words)


if __name__ == "__main__":
    app = App()
    try:
        app.start()
    except KeyboardInterrupt:
        app.save_statistic()
