cooling_type_limits = {
    "HI_ACTIVE_COOLING": {'lower_limit': 0, 'upper_limit': 45},
    "MED_ACTIVE_COOLING": {'lower_limit': 0, 'upper_limit': 40},
    "PASSIVE_COOLING": {'lower_limit': 0, 'upper_limit': 35},
}

email_alert_message = {"TOO_LOW": {'receiver_address': 'recepient_address@organisation.com',
                                   'alert_message': "Temperature is too low. Requesting immediate action"},
                       "TOO_HIGH": {'receiver_address': 'recepient_address@organisation.com',
                                    'alert_message': "Temperature is too high. Requesting immediate action"}
                       }


def check_and_alert(alert_target, battery_char, temperature_in_Celsius):
    breach_type = \
        classify_temperature_breach(battery_char['coolingType'], temperature_in_Celsius)
    if breach_type != "NORMAL":
        return target_alert[alert_target](breach_type)


def classify_temperature_breach(cooling_type, temperature_in_celsius):
    if check_if_input_is_valid(cooling_type, temperature_in_celsius):
        cooling_temp_range = cooling_type_limits[cooling_type]
        return infer_breach(temperature_in_celsius, cooling_temp_range['lower_limit'],
                            cooling_temp_range['upper_limit'])
    else:
        return 'INVALID_INPUT'


def check_if_input_is_valid(cooling_type, temperature_in_celsius):
    if cooling_type in cooling_type_limits.keys() and temperature_in_celsius is not None:
        return True
    return False


def infer_breach(value, lower_limit, upper_limit):
    if value < lower_limit:
        return 'TOO_LOW'
    if value > upper_limit:
        return 'TOO_HIGH'
    return 'NORMAL'


def send_to_controller(breach_type):
    header = 0xfeed
    print(f'{header}, {breach_type}')
    return "CONTROLLER_ACTIVATED"


def send_to_email(breach_type):
    email_message = email_alert_message[breach_type]
    email_data = f"To {email_message['receiver_address']},\n \t Hello, \n \t {email_message['alert_message']}"
    print(email_data)
    return "EMAIL_SENT"


target_alert = {
    'email': send_to_email,
    'controller': send_to_controller
}
