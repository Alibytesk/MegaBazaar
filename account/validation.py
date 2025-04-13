from django import forms

class PasswordValidation:
    @staticmethod
    def password_validation(password):
        special_character, errors = "!@#$%^&*", list()
        if len(password) < 8:
            errors.append('password must be at least 8 character')
        if not any(i in special_character for i in password):
            errors.append('password must contain at least one special character')
        if not any(i.isupper() for i in password):
            errors.append('password must contain at least one uppercase letter')
        if not any(i.islower() for i in password):
            errors.append('password must contain at least one lowercase letter')
        if not any(i.isdigit() for i in password):
            errors.append('password must contain at least one number')

        if not errors:
            return password
        else:
            raise forms.ValidationError(errors)

class PhoneValidator:
    @staticmethod
    def is_phone_start_with_09(phone: str):
        if not phone.startswith('09'):
            raise forms.ValidationError('phone should start with 09 numbers')