class PourProgress:
    WILL_CALL = "will call"
    SCHEDULED = "scheduled"
    CANCELED = "canceled"
    IN_PROGRESS = "in_progress"
    RELEASED = "released"
    COMPLETE = "complete"

    choices = [
        (WILL_CALL, "will call"),
        (SCHEDULED, "scheduled"),
        (CANCELED, "canceled"),
        (IN_PROGRESS, "in_progress"),
        (RELEASED, "released"),
        (COMPLETE, "complete"),
    ]


class StatusChoices:
    """choices for status field

    Args:
        SCHEDULED   (str):  scheduled
        IN_PROGRESS (str):  in progress
        COMPLETE    (str):  complete
        choices     (list): Tuples of above -> (key, value) pairs
    """

    SCHEDULED = "scheduled"
    IN_PROGRESS = "in progress"
    COMPLETE = "complete"

    choices = [
        (SCHEDULED, "scheduled"),
        (IN_PROGRESS, "in progress"),
        (COMPLETE, "complete"),
    ]
