__author__ = 'root'
# coding=utf-8
import changeview

class AlarmTemp:
    # Device id
    dev_id = -1

    # Action
    action = ''

    # Condition
    condition = ''

    # Temp Value
    temp_value = -1

    # Flag Active
    active = False

    def __unicode__(self):
        if self.condition == '':
            return ''

        string = 'Auto %s %s %s %s °C' %(changeview.change_action_view(self.action), self.condition, self.temp_value)
        return string





