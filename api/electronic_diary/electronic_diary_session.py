from requests import Session, Response

from api.electronic_diary.electronic_diary import UsualDiaryOneWeek, UsualDiaryOneDay, UsualDiaryOneSubject
from api.electronic_diary.electronic_diary_errors import WrongLoginOrPasswordError
from api.electronic_diary.electronic_diary_parser import *
from api.electronic_diary.electronic_diary_user import ElectronicDiaryUser

import datetime


class ElectronicDiarySession(Session):
    """Special wrapper of request.Session for more comfortable work with the data
    of the user of the "https://elschool.ru/"

    Attributes
    ----------

    REGISTRATION_URL: str
        Url address for registration is stored here
    PRIVATE_OFFICE_URL: str
        Url address for private office of the user
    DIARY_USUAL_URL: str
        Url address for the page with the diary of the user
    DIARY_GRADES_URL: str
        Url address for the page with marks on each subject for the user
    DIARY_GRADES_AND_ABSENCES_URL: str
        Url address for the page with mark and absences on each subject for the user
    DIARY_RESULTS_URL: str
        Url address for the page with result of the quarter and year on each subject for the user

    USER_AGENT: str
        Value for key "user-agent" in http request headers
    _user: ElectronicDiaryUser
        Object representing user

    METHODS
    -------
    _register_user() -> None
        Registers user.
    _set_user_metadata() -> None
        Finds school_id, district_id, class_id and id of the user and sets them in user.meta
    _set_headers_user_agent() -> None
        We need to update user-agent parameter in http requests after each request
    _get_diary_usual() -> UsualDiaryOneWeek
        Returns object representing usual diary of the user
    _get_diary_usual_response() -> Response
        Returns html response with the diary usual marking
    _check_for_success_registration(response: Response) -> None
        Static method that checks if password and login is correct.
    tell_about_user()
        Returns string representing user
    tell_about_usual_diary()
        Returns string representing diary of the user
    """

    REGISTRATION_URL = 'https://elschool.ru/Logon/Index'
    PRIVATE_OFFICE_URL = 'https://elschool.ru/users/privateoffice'
    DIARY_USUAL_URL = 'https://elschool.ru/users/diaries/details'
    DIARY_GRADES_URL = 'https://elschool.ru/users/diaries/grades'
    DIARY_GRADES_AND_ABSENCES_URL = 'https://elschool.ru/users/diaries/gradesandabsences'
    DIARY_RESULTS_URL = 'https://elschool.ru/users/diaries/results'

    USER_AGENT = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) ' \
                 'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                 'Chrome/83.0.4103.116 Mobile ' \
                 'Safari/537.36'

    def __init__(self, user_login: str, user_password: str) -> None:
        """Init method that sets registers user and sets his basic info

        Arguments
        ---------
        user_login: str
            User login from account of https://elschool.ru/
        user_password: str
            User password from account of https://elschool.ru/

        Raises
        ------
        WrongLoginOrPasswordError
            if login or password of the user is wrong

        Returns
        ------
        None
        """

        super().__init__()
        self._user = ElectronicDiaryUser(user_login, user_password)  # Object representing user
        self._set_headers_user_agent()  # To make page think that we are not a robot
        self._register_user()  # Registering user with the given login and password
        self._set_user_metadata()  # Finding info about user school and his id

    def _register_user(self) -> None:
        """Method that registers user.

        Raises
        ------
        WrongLoginOrPasswordError
            if login or password of the user is wrong

        Returns
        -------
        None
        """

        # Creating dict for GET request with login and password
        data = {
            'login': self._user._login,
            'password': self._user._password
        }
        response = self.post(self.REGISTRATION_URL, data=data)  # Http request

        # It raises WrongLoginOrPasswordError if login or password is wrong
        self._check_for_success_registration(response)

    def _set_user_metadata(self) -> None:
        """Finds important values for user, such as: district_id, school_id, class_id, user_id and name.
        User must be authenticated to use this method"""

        self._set_headers_user_agent()
        response = self.get(self.PRIVATE_OFFICE_URL)  # Http response from user private office
        meta = get_metadata_from_private_office(response.text)  # Getting metadata for user

        # Setting found values
        self._user._name = meta.user_name
        self._user._meta.id = meta.user_id
        self._user._meta.district_id = meta.district_id
        self._user._meta.school_id = meta.school_id
        self._user._meta.class_id = meta.class_id

    def _set_headers_user_agent(self) -> None:
        """Function that sets user-agent value in http request
        to make page think that we are not a robot.
        We need it to update that value after every request"""

        self.headers['user-agent'] = self.USER_AGENT

    def _get_diary_usual(self, year: int, month: int, day: int) -> UsualDiaryOneWeek:
        """Returns usual diary (subject, homework, grades for each day) in a dictionary

        Arguments
        ---------
        year: int
            Year of the requested page
        month: int
            Month of the requested page
        day: int
            Day of the requested page

        Returns
        -------
        UsualDiaryOneWeek
            object describing usual diary of the user"""

        # We need that parameter to do http request
        # If finds the needed page of the diary
        week_number = datetime.date(year, month, day).isocalendar()[1]

        response = self._get_diary_usual_response(year, week_number)  # Getting http response from user private office

        days = get_diary_days(response.text)  # Diary days
        diary_week = UsualDiaryOneWeek()

        for day in days:
            # Getting data for one day
            date = get_date_from_diary_day(day)
            subjects = get_subjects_from_diary_day(day)

            # Creating object describing one week in the diary
            diary_day = UsualDiaryOneDay(date)
            diary_week.add_day(diary_day)

            if check_for_no_lesson(day):  # Checks if there are no lesson that day
                diary_day.no_lesson = True
                continue

            for subject in subjects:
                # Getting data for one subject
                meta = get_subject_data(subject)
                diary_subject = UsualDiaryOneSubject(meta.subject_name, meta.subject_type,
                                                     meta.subject_time, meta.subject_homework,
                                                     meta.subject_marks)
                diary_day.add_subject(diary_subject)

        return diary_week

    def _get_diary_usual_response(self, year: int, week_number: int) -> Response:
        """Gets raw html from user diary with the given arguments

        Arguments
        ---------
        year:int
            Year of the requested page of the diary
        week_number: int
            Week of the requested page of the diary
        """

        self._set_headers_user_agent()  # Updating user-agent parameter

        # Http request parameters
        request_params = {
            'rooId': self._user._meta.district_id,
            'instituteId': self._user._meta.school_id,
            'departmentId': self._user._meta.class_id,
            'pupilId': self._user._meta.id,
            'year': year,
            'week': week_number,
            'log': 'false'
        }
        return self.get(self.DIARY_USUAL_URL, params=request_params)  # Http response from user usual diary

    @staticmethod
    def _check_for_success_registration(response: Response) -> None:
        """Checks if the registration was successful

        Arguments
        ---------
        response: Response
            Response of the http request

        Raises
        ------
        WrongLoginOrPasswordError
            if login or password is incorrect
        """

        personal_data = get_field_of_success_registration(response.text)
        if personal_data is None:  # If there is no block with user data it means that registration were unsuccessful
            raise WrongLoginOrPasswordError

    def get_user(self) -> ElectronicDiaryUser:
        return self._user

    def get_usual_diary(self) -> UsualDiaryOneWeek:
        """That methods shows us current page of the diary"""

        current_date = datetime.datetime.now()
        return self._get_diary_usual(year=current_date.year, month=current_date.month, day=current_date.day)
