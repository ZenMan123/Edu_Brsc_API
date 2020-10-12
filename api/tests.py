import pytest

from api.electronic_diary.electronic_diary_session import ElectronicDiarySession
from api.electronic_diary.electronic_diary_errors import WrongLoginOrPasswordError


def test_wrong_login_or_password():
    with pytest.raises(WrongLoginOrPasswordError):
        session = ElectronicDiarySession('WrongPassword', 'WrongPassword')


def test_usual_case():
    session = ElectronicDiarySession('CORRECT_LOGIN', 'CORRECT_PASSWORD')
    session.get_user()
    session.get_usual_diary()
