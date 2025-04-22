import pytest
from contextlib import nullcontext as does_not_raise

from email_validator import EmailSyntaxError


class TestUser:
    @pytest.mark.parametrize(
        'username, email, password, expectation',
        [
            ('boben', 'boben@gmail.com', 'Qwerty12', does_not_raise()),
            ('steve', 'ail.com', 'Qwerty12', pytest.raises(EmailSyntaxError)),
            ('e', 'e@gmail.com', 'Qwerty12', pytest.raises(TypeError)),
            ('alice', 'alice@gmail.com', 'qwerty', pytest.raises(TypeError)),
        ]
    )
    def test_create_user(self, username, email, password, expectation):
        with expectation:
            pass

    def test_get_user(self, id_or_username):
        pass

    def test_update_user(self, user_id):
        pass

    def test_delete_user(self, user_id):
        pass