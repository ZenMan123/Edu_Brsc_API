from meta import Meta


class ElectronicDiaryUser:
    """Class representing the user of the "https://elschool.ru/"

    Attributes
    ----------
    Name: str
        Name of the user (it should be defined after registration)
    login: str
        Login of the user
    password: str
        Password of the user
    meta: Meta
        Object for keeping metadata of the user (user_id, school_id, district_id, etc.)
    """

    def __init__(self, login: str, password: str) -> None:
        self.name = ''
        self.login = login
        self.password = password
        self.meta = Meta()

    def __str__(self) -> str:
        """Method showing info about user"""

        return f'Name: {self.name}\n' \
               f'Id: {self.meta.id}\n' \
               f'District_id: {self.meta.district_id}\n' \
               f'School_id: {self.meta.school_id}\n' \
               f'Class_id: {self.meta.class_id}'

