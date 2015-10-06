__author__ = 'root'


def change_action_view(action):
    if action is None or action == '':
        return ''

    if action == 'on':
        return 'ON'
    else:
        return 'OFF'
