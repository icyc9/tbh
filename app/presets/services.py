from app.presets.presets import MESSAGE_LIST
from app.exceptions import PresetError


def get_preset_by_code(code):

    for index, item in enumerate(MESSAGE_LIST['presets']):
        if item['code'] == code:
            return item['message']

    raise PresetError('Preset does not exist')