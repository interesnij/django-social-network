import string

words = ["дурак", "кретин"]

def distance(a, b):
    "Вычисляет расстояние Левенштейна между a и b."
    n, m = len(a), len(b)
    if n > m:
        a, b = b, a
        n, m = m, n

    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if a[j - 1] != b[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]

def is_have_bad_words(text):
    d = {'а' : ['а', 'a', '@'],
      'б' : ['б', '6', 'b'],
      'в' : ['в', 'b', 'v'],
      'г' : ['г', 'r', 'g'],
      'д' : ['д', 'd'],
      'е' : ['е', 'e'],
      'ё' : ['ё', 'e'],
      'ж' : ['ж', 'zh', '*'],
      'з' : ['з', '3', 'z'],
      'и' : ['и', 'u', 'i'],
      'й' : ['й', 'u', 'i'],
      'к' : ['к', 'k', 'i{', '|{'],
      'л' : ['л', 'l', 'ji'],
      'м' : ['м', 'm'],
      'н' : ['н', 'h', 'n'],
      'о' : ['о', 'o', '0'],
      'п' : ['п', 'n', 'p'],
      'р' : ['р', 'r', 'p'],
      'с' : ['с', 'c', 's'],
      'т' : ['т', 'm', 't'],
      'у' : ['у', 'y', 'u'],
      'ф' : ['ф', 'f'],
      'х' : ['х', 'x', 'h' , '}{'],
      'ц' : ['ц', 'c', 'u,'],
      'ч' : ['ч', 'ch'],
      'ш' : ['ш', 'sh'],
      'щ' : ['щ', 'sch'],
      'ь' : ['ь', 'b'],
      'ы' : ['ы', 'bi'],
      'ъ' : ['ъ'],
      'э' : ['э', 'e'],
      'ю' : ['ю', 'io'],
      'я' : ['я', 'ya']
    }
    for key, value in d.items():
        for letter in value:
            for phr in text:
                if letter == phr:
                    text = text.replace(phr, key)

    for word in words:
        for part in range(len(text)):
            fragment = text[part: part+len(word)]
            if distance(fragment, word) <= len(word)*0.25:
                return False
