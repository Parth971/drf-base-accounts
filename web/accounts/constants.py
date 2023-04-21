# Error
PASSWORD_MISMATCH = "Password fields didn't match"
INVALID_EMAIL = "Email not valid"
INCORRECT_OLD_PASSWORD = "Old password is not correct"
PASSWORD_SPECIAL_SYMBOL_ERROR = 'Password must contain at-least one special symbol'
PASSWORD_DIGIT_ERROR = 'Password must contain at-least one digit'
PASSWORD_UPPERCASE_LETTER_ERROR = 'Password must contain at-least one uppercase letter'
PASSWORD_LOWERCASE_LETTER_ERROR = 'Password must contain at-least one lowercase letter'
FIRST_NAME_ERROR = 'First name must contain alphabets and space only'
LAST_NAME_ERROR = 'Last name must contain alphabets and space only'
FIRST_NAME_LENGTH_ERROR = 'First name should have length between 3 to 20'
LAST_NAME_LENGTH_ERROR = 'Last name should have length between 3 to 20'
INVALID_PHONE_NUMBER = 'Mobile number is not valid'
EMAIL_NOT_ACTIVATED = "Email is not active"

# Help text
PASSWORD_HELP_TEXT = 'Password must contain 1 special char, 1 digit, 1 small alphabet, and 1 capital alphabet'

# Validation Regex
SPECIAL_SYMBOL_REGEX = "(?=.*?[#?!@$%^&*-])"
DIGIT_REGEX = "(?=.*?[0-9])"
UPPERCASE_LETTER_REGEX = "(?=.*?[A-Z])"
LOWERCASE_LETTER_REGEX = "(?=.*?[a-z])"
USER_NAME_REGEX = "^[a-zA-Z ]+$"  # Used for both first_name and last_name field in User model
PHONE_NUMBER_REGEX = "^\\+?[1-9][0-9]{7,14}$"

# Message
RESTORE_PASSWORD_LINK_SENT = "Restore password link has been sent to email"

# Variables
FIRST_NAME_MINIMUM_LENGTH = LAST_NAME_MINIMUM_LENGTH = 3
FIRST_NAME_MAXIMUM_LENGTH = LAST_NAME_MAXIMUM_LENGTH = 20
