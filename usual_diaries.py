class UsualDiaryOneSubject:
    """Class representing one subject in user diary

    Arguments
    ---------
    name: str
        Name of the subject
    type: str
        Type of the lesson (intramural, extramural)
    time: str
        Time of the lesson (8:00 - 8:45)
    homework: str
        Homework for this lesson
    marks: str
        Marks for that lesson

    Returns
    -------
    None
    """

    def __init__(self, name: str, stype: str, time: str, homework: str, marks: str) -> None:
        self.name = name
        self.type = stype  # (intramural, extramural)
        self.time = time
        self.homework = homework
        self.marks = marks

    def __str__(self) -> str:
        return f'{self.name}, Type: {self.type}, Time: {self.time}, Homework: {self.homework}, Marks: {self.marks}'


class UsualDiaryOneDay:
    """Class representing one day in user diary

    Arguments
    ---------
    date: str
        Date of the lesson (f.e. понедельник 13.05)
    subjects: list
        Array of subjects that day
    no_lesson: bool
        Bool variable indicating absence of lessons

    Methods
    -------
    add_subject(subject: UsualDiaryOneSubject) -> None
        Adds subject to that day

    Returns
    -------
    None
    """

    def __init__(self, date: str, no_lesson: bool = False) -> None:
        self.date = date
        self.subjects = []
        self.no_lesson = no_lesson

    def add_subject(self, subject: UsualDiaryOneSubject) -> None:
        """Adds subject to the list of subjects"""

        self.subjects.append(subject)

    def __getitem__(self, ind: int) -> UsualDiaryOneSubject:
        """Returns requested subject"""

        return self.subjects[ind - 1]

    def __str__(self):
        """Method showing one day timetable

        Example
        -------
        Расписание на понедельник 13.05
        1) математика 8:00 - 8:45
        2) русский язык 8:50 - 9:35
        и т.д
        """

        result = [f'Расписание на {self.date}:']

        if self.no_lesson:  # Checks if there are no lessons that day
            result.append('Занятий нет')
            return '\n'.join(result)

        for i in range(len(self.subjects)):  # Adding description for subjects
            result.append(str(self.subjects[i]))
        return '\n'.join(result)


class UsualDiaryOneWeek:
    """Object representing one week in user diary

    Arguments
    ---------
    days: list
        Array of days of that week

    Methods
    -------
    add_day(one_day_diary: UsualDiaryOneDay) -> None
        Adds a day to the list of days

    Returns
    -------
    None

    """

    def __init__(self):
        self.days = []

    def add_day(self, one_day_diary: UsualDiaryOneDay) -> None:
        """Adds one day to the diary"""

        self.days.append(one_day_diary)

    def __getitem__(self, ind: int) -> UsualDiaryOneDay:
        """Returns requested day"""

        return self.days[ind - 1]

    def __str__(self):
        """Returns week data

        Example
        -------
        {Описание дня 1}



        {Описание дня 2}

        и т.д.
        """

        result = []
        for i in self.days:
            result.append(i.__str__())
        return '\n\n\n'.join(result)
