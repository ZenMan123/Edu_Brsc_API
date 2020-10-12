# API for https://elschool.ru/
---

Этот проект предоставляет возможность удобно получать данные из электронного дневника https://elschool.ru/.
Например, для получения дневника с расписанием, домашкой и оценками достаточно написать:
```python
from api.electronic_diary.electronic_diary_session import ElectronicDiarySession

session = ElectronicDiarySession(USER_LOGIN, USER_PASSWORD)
print(session.get_usual_diary())
```
А для того чтобы просто получить дневник и удобно с ним работать можно написать:
```python
from api.electronic_diary.electronic_diary_session import ElectronicDiarySession

session = ElectronicDiarySession(USER_LOGIN, USER_PASSWORD)
diary = session.get_usual_diary()

# Узнаем что будет во вторник
tuesday = diary[2]  # 1 - Пн, 2 - Вт, 3 - Ср и т.д.

# Проверяем наличие уроков в этот день
print(tuesday.no_lesson)

# Узнаем предметы, которые будут проходить во вторник
for subject in tuesday.subjects:
    print(subject)

# Узнаем третий урок во вторник
third_subject_on_tuesday = tuesday[3]
print(third_subject_on_tuesday)

# Узнаем дз на этот урок
print(third_subject_on_tuesday.homework)
```

Также, есть возможность посмотреть основную информацию о пользователе:
```python
from api.electronic_diary.electronic_diary_session import ElectronicDiarySession

session = ElectronicDiarySession(USER_LOGIN, USER_PASSWORD)
print(session.get_user())
```
---

В будущем также планируется добавить API и для других функций сайта.
Например, просмотр табелей или сообщений.
