# pylint: disable=E0401

# skipcq
"""
Various small commands
"""
import os
import re
import sys

from rich import pretty
from rich.console import Console
from textblob import TextBlob

pretty.install()
console = Console()

countries = ['afghanistan', 'albania', 'algeria', 'american samoa', 'andorra', 'angola', 'anguilla', 'antarctica', 'antigua and barbuda', 'argentina', 'armenia', 'aruba', 'australia', 'austria', 'azerbaijan', 'bahamas', 'bahrain', 'bangladesh', 'barbados', 'belarus', 'belgium', 'belize', 'benin', 'bermuda', 'bhutan', 'bolivia', 'bosnia and herzegovina', 'botswana', 'bouvet island', 'brazil', 'british indian ocean territory', 'brunei darussalam', 'bulgaria', 'burkina faso', 'burundi', 'cambodia', 'cameroon', 'canada', 'cape verde', 'cayman islands', 'central african republic', 'chad', 'chile', 'china', 'christmas island', 'cocos (keeling) islands', 'colombia', 'comoros', 'congo', 'congo, the democratic republic of', 'cook islands', 'costa rica', "cã”te d'ivoire", 'croatia', 'cuba', 'cyprus', 'czech republic', 'denmark', 'djibouti', 'dominica', 'dominican republic', 'ecuador', 'egypt', 'el salvador', 'equatorial guinea', 'eritrea', 'estonia', 'ethiopia', 'falkland islands (malvinas)', 'faroe islands', 'fiji', 'finland', 'france', 'french guiana', 'french polynesia', 'french southern territories', 'gabon', 'gambia', 'georgia', 'germany', 'ghana', 'gibraltar', 'greece', 'greenland', 'grenada', 'guadeloupe', 'guam', 'guatemala', 'guinea', 'guinea', 'guyana', 'haiti', 'heard island and mcdonald islands', 'honduras', 'hong kong', 'hungary', 'iceland', 'india', 'indonesia', 'iran, islamic republic of', 'iraq', 'ireland', 'israel', 'italy', 'jamaica', 'japan', 'jordan', 'kazakhstan', 'kenya', 'kiribati', "korea, democratic people's republic of", 'korea, republic of', 'kuwait', 'kyrgyzstan', "lao people's democratic republic", 'latvia', 'lebanon', 'lesotho', 'liberia', 'libyan arab jamahiriya', 'liechtenstein', 'lithuania', 'luxembourg', 'macao', 'macedonia, the former yugoslav republic of', 'madagascar', 'malawi', 'malaysia', 'maldives', 'mali', 'malta', 'marshall islands', 'martinique', 'mauritania', 'mauritius', 'mayotte', 'mexico', 'micronesia, federated states of', 'moldova, republic of', 'monaco', 'mongolia', 'montserrat', 'morocco', 'mozambique', 'myanmar', 'namibia', 'nauru', 'nepal', 'netherlands', 'netherlands antilles', 'new caledonia', 'new zealand', 'nicaragua', 'niger', 'nigeria', 'niue', 'norfolk island', 'northern mariana islands', 'norway', 'oman', 'pakistan', 'palau', 'palestinian territory, occupied', 'panama', 'papua new guinea', 'paraguay', 'peru', 'philippines', 'pitcairn', 'poland', 'portugal', 'puerto rico', 'qatar', 'rã‰union', 'romania', 'russian federation', 'rwanda', 'saint helena', 'saint kitts and nevis', 'saint lucia', 'saint pierre and miquelon', 'saint vincent and the grenadines', 'samoa', 'san marino', 'sao tome and principe', 'saudi arabia', 'senegal', 'serbia and montenegro', 'seychelles', 'sierra leone', 'singapore', 'slovakia', 'slovenia', 'solomon islands', 'somalia', 'south africa', 'south georgia and south sandwich islands', 'spain', 'sri lanka', 'sudan', 'suriname', 'svalbard and jan mayen', 'swaziland', 'sweden', 'switzerland', 'syrian arab republic', 'taiwan, province of china', 'tajikistan', 'tanzania, united republic of', 'thailand', 'timor', 'togo', 'tokelau', 'tonga', 'trinidad and tobago', 'tunisia', 'turkey', 'turkmenistan', 'turks and caicos islands', 'tuvalu', 'uganda', 'ukraine', 'united arab emirates', 'united kingdom', 'united states', 'united states minor outlying islands', 'uruguay', 'uzbekistan', 'vanuatu', 'viet nam', 'virgin islands, british', 'virgin islands, u.s.', 'wallis and futuna', 'western sahara', 'yemen', 'zimbabwe']


def print_custom(text: str, st: str = None):
    """Wrapper"""
    console.print(text, end='', style=st)


def choice_selector(argument):
    """Replacement for switch-case function"""
    switcher = {
        1: "one",
        2: "two",
        3: "three",
        4: "four",
    }
    return switcher.get(argument, "Invalid Choice")


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS  # skipcq: PYL-W0212
    except Exception:  # skipcq: PYL-W0703
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def correction(data):
    """Spellcheck"""
    text = TextBlob(data)
    text = text.correct()
    return str(text)


def get_field_index(field: str) -> int:
    f = field
    switcher = {
        "Name": 0,
        "Username": 1,
        "Country": 2,
        "Email": 3,
        "Password": 4
    }
    i = switcher.get(f, 10)
    return i


def checkmail(email: str) -> bool:
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.match(regex, email):
        return True
    return False


def countries_exist(val: str):
    """Checks if country exists"""
    c = val.lower()
    if c in countries:
        return True
    return False
