from api.meta import Meta


class ElectronicDiaryUser:
    """Class representing the user of the "https://elschool.ru/"

    Attributes
    ----------
    _name: str
        Name of the user (it should be defined after registration)
    login: str
        Login of the user
    password: str
        Password of the user
    _meta: Meta
        Object for keeping metadata of the user (user_id, school_id, district_id, etc.)

    Methods
    -------
    get_name() -> str
        Returns a name of the user
    """

    def __init__(self, login: str, password: str) -> None:
        self._name = ''
        self._login = login
        self._password = password
        self._meta = Meta()

    def get_name(self) -> str:
        return self._name

    def __str__(self) -> str:
        """Method showing info about user"""

        return f'Name: {self._name}\n' \
               f'Id: {self._meta.id}\n' \
               f'District_id: {self._meta.district_id}\n' \
               f'School_id: {self._meta.school_id}\n' \
               f'Class_id: {self._meta.class_id}'

