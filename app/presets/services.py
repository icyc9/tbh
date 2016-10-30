from app.presets.presets import MESSAGE_LIST


def get_preset_by_code(code):

    for index, item in enumerate(MESSAGE_LIST['presets']):
        if item['code'] == code:
            return item['message']

    raise Exception('Preset does not exist')