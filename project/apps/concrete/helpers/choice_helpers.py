
class MixChoices:
    RICH = 'rich'
    STANDARD = 'standard'
    MEDIUM = 'medium'
    LEAN = 'lean'

    choices = [
        (RICH, 'rich'),
        (STANDARD, 'standard'),
        (MEDIUM, 'medium'),
        (LEAN, 'lean'),
    ]


class TempDelay:
    NONE = None
    HIGH = 'high'
    LOW = 'low'

    choices = [
        (NONE, None),
        (HIGH, 'high'),
        (LOW, 'low'),
    ]

class PrecipDelay:
    CLEAR = None
    RAIN = 'rain'
    SNOW = 'snow'

    choices = [
        (CLEAR, None),
        (RAIN, 'rain'),
        (SNOW, 'snow'),
    ]


class PourProgress:
    WILL_CALL = 'will call'
    CANCELED = 'canceled'
    IN_PROGRESS = 'in_progress'
    RELEASED = 'released'
    COMPLETE = 'complete'
    
    choices = [
        (WILL_CALL, 'will call'),
        (CANCELED, 'canceled'),
        (IN_PROGRESS, 'in_progress'),
        (RELEASED, 'released'),
        (COMPLETE, 'complete'),
    ]
