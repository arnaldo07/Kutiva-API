# utils.py by Arnaldo Govene [arnaldo.govene@outlook.com]
# Contains basic independent functions
# Copyrighth 2016 Xindiri, LLC

from passlib.apps import custom_app_context as pwd_context

class Utils():

    # Encrypts password
    def password_hash(self, password):
        self._hashed_password = pwd_context.encrypt(password)
        return self._hashed_password

    # Verify password
    def password_verify(self, password):
        return pwd_context.verify(password, self._hashed_password)
