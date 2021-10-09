from tkinter.messagebox import showerror

from accessify import protected


class Validator:

    entries = None

    @protected
    def _field_empty_validator(self, key, field):
        if str(key).strip() == '':
            showerror(title='error', message=f"'key' = {str(key) != ''} Empty field: 'field' = key")
            raise ValueError(f"'key' = {str(key) != ''} Empty field: 'field' = key")
        if str(self.entries[field].get()).strip() == '':
            showerror(title='error', message=f"'key' = {key} Empty field: {field}")
            raise ValueError(f"'key' = {key} Empty field: {field}")

    @protected
    def _field_integer_validator(self, key, field, validate_field: list):
        if field in validate_field and not str(self.entries[field].get()).strip().isdigit():
            showerror(title='error', message=f"is not a number: 'key' = {key}, 'field' = {field}")
            raise ValueError(f"is not a number: {key, field}")
