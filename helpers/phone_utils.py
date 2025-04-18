# File: helpers/phone_utils.py

import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException

def normalize_phone_number(phone_number: str, region: str = "SA") -> str:
    """
    Normalize the given phone number to the E.164 format.
    
    If the phone number does not start with a '+', this function assumes the user
    is entering a local Saudi number. In that case, if the number starts with a "0",
    the leading zero is removed and the country code "+966" is prepended.
    
    This ensures that users on mobile (especially on iOS) don’t have to type the country code.
    
    Raises a ValueError if the number is invalid.
    """
    # Strip any surrounding whitespace.
    phone_number = phone_number.strip()
    
    # If the number does not start with '+', assume it's a local number.
    if not phone_number.startswith('+'):
        # Remove a leading 0 if present.
        if phone_number.startswith('0'):
            phone_number = phone_number[1:]
        # Prepend Saudi Arabia's country code.
        phone_number = f"+966{phone_number}"
    
    try:
        # Parse the phone number using the provided region.
        parsed_number = phonenumbers.parse(phone_number, region)
        # Check that the number is valid.
        if not phonenumbers.is_valid_number(parsed_number):
            raise ValueError("Invalid phone number.")
        # Return the formatted number in E.164 format.
        return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
    except NumberParseException as e:
        raise ValueError(f"Error parsing phone number: {e}")
