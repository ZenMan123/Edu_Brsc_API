from bs4 import BeautifulSoup
from api.meta import Meta

from typing import List

"""All the functions here parse html pages and return requested data

Functions
---------
get_diary_days(html_code: str) -> List[BeautifulSoup]
    Gets parts of html code describing a particular day in a diary
get_subjects_from_diary_day(html_code: str) -> List[BeautifulSoup]
    Gets parts of html code describing a particular subject in a diary
check_for_no_lesson(html_code: str) -> bool
    Checks if there is a block of lesson absence
get_date_from_diary_day(html_code: str) -> str
    Get date from one particular day
get_subject_data(html_code: str) -> Meta
    Gets subject data (name, time, type, etc.)
get_metadata_from_private_office(html_code: str) -> Meta
    Gets user metadata (school_id, district_id, etc.)
get_field_of_success_registration(html_code: str) -> BeautifulSoup
    Looks for field of success registration
"""


def get_diary_days(html_code: str) -> List[BeautifulSoup]:
    soup = BeautifulSoup(html_code, features='html.parser')  # Html parser

    # Two parts of the week
    half_of_weeks = soup.find('div', {'class': 'diaries'}).find_all('div', {'class': 'col-6'})[:2]

    days = []
    for half in half_of_weeks:  # Select days from each part of the week and insert them
        days.extend(half.find('table', {'class': 'table table-bordered'}).find_all('tbody'))

    return days


def get_subjects_from_diary_day(soup: BeautifulSoup) -> List[BeautifulSoup]:
    return soup.find_all('tr', {'class': 'diary__lesson'})


def check_for_no_lesson(soup: BeautifulSoup) -> bool:
    return True if soup.find('td', {'class': 'diary__nolesson'}) else False


def get_date_from_diary_day(soup: BeautifulSoup) -> str:
    return soup.find('td', {'class': 'diary__dayweek'}).find('p').text


def get_subject_data(soup: BeautifulSoup) -> Meta:
    try:
        subject_name = soup.find('div', {'class': 'flex-grow-1'}).text
    except AttributeError:
        subject_name = ''

    try:
        subject_time = soup.find('div', {'class': 'diary__discipline__time'}).text
    except AttributeError:
        subject_time = ''

    try:
        subject_type = soup.find('div', {'class': 'lesson-form'}).text
    except AttributeError:
        subject_type = ''

    try:
        subject_homework = soup.find('div', {'class': 'diary__homework-text'}).text
    except AttributeError:
        subject_homework = ''

    try:
        subject_marks = soup.find('span', {'class': 'diary__mark', 'model-type': 'mark'}).text
    except AttributeError:
        subject_marks = ''

    meta = Meta()
    meta.subject_name = subject_name
    meta.subject_type = subject_type
    meta.subject_time = subject_time
    meta.subject_homework = subject_homework
    meta.subject_marks = subject_marks

    return meta


def get_metadata_from_private_office(html_code: str) -> Meta:
    soup = BeautifulSoup(html_code, features='html.parser')  # Http parser

    # Finding element with district_id, school_id and class_id
    user_metadata_element = soup.find('table', {'style': "table-layout: fixed; width: 100%;"}).find('a')
    user_metadata = user_metadata_element.get('href').split('/')

    # Finding element with username and his id
    user_name_and_id_element = soup.find('div', {'href': "/users/privateoffice/edit", 'class': "personal-data"})
    user_name = user_name_and_id_element.find('h3').text
    user_id = user_name_and_id_element.find('td', {'class': 'personal-data__info-value '
                                                            'personal-data__info-value_bold'}).text

    meta = Meta()
    meta.user_name = user_name
    meta.user_id = user_id
    meta.district_id = user_metadata[2]
    meta.school_id = user_metadata[4]
    meta.class_id = user_metadata[6]

    return meta


def get_field_of_success_registration(html_code: str) -> BeautifulSoup:
    soup = BeautifulSoup(html_code, features="html.parser")  # Creating parser
    return soup.find('div', {'class': 'personal-data-wrapper'})  # Looking for object with user data
