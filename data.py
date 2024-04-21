import json
DICT_DATA = 'quiz_data'
quiz_data = [
    {
        'question': 'Что такое Python?',
        'options': ['Язык программирования', 'Тип данных', 'Музыкальный инструмент', 'Змея на английском'],
        'correct_option': 0
    },
    {
        'question': 'Какой тип данных используется для хранения целых чисел?',
        'options': ['int', 'float', 'str', 'natural'],
        'correct_option': 0
    },
    {
        'question': 'В каком году Гагарин полетел в космос?',
        'options': ['1965', '1963', '1961', '1962'],
        'correct_option': 2
    },
    {
        'question': 'Зимой и летом одним цветом?',
        'options': ['Роза', 'Береза', 'Заяц', 'Елка'],
        'correct_option': 3
    },
    {
        'question': 'Кто проживает на дне океана?',
        'options': ['Сом', 'Спанч-Боб', 'Окунь', 'Камень'],
        'correct_option': 1
    },
    {
        'question': 'Сколько будет 2 + 2 * 2?',
        'options': ['6', '8', '4', '10'],
        'correct_option': 0
    },
    {
        'question': 'Когда заходил самый лучший день, по мнению Лепса?',
        'options': ['в четверг', 'в прошлом году', 'вчера', 'в сентябре'],
        'correct_option': 2
    },
    {
        'question': 'А и Б сидели на требе, А упала, Б  пропала, кто остался на трубе?',
        'options': ['Никого', 'Б', 'и', 'А'],
        'correct_option': 2
    },
    {
        'question': 'Кто уничтожил кольцо всевластия?',
        'options': ['Бильбо', 'Фродо', 'Леголас', 'Сэм'],
        'correct_option': 1
    },
    {
        'question': 'Главой какой деревни стал Наруто?',
        'options': ['Листа', 'Песка', 'Дождя', 'Камня'],
        'correct_option': 0
    }
]


with open(DICT_DATA, 'w') as file:
    json.dump(quiz_data, file)