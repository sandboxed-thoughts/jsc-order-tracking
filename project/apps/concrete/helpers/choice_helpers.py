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


class GarageChoices:
    NONE = None
    FT4 = "4'"
    FT8 = "8'"
    FT9 = "9'"

    choices = [
        (NONE, None),
        (FT4, "4'"),
        (FT8, "8'"),
        (FT9, "9'"),
    ]


# not used, not imported:

# class TempDelay:
#     NONE = None
#     HIGH = "high"
#     LOW = "low"

#     choices = [
#         (NONE, None),
#         (HIGH, "high"),
#         (LOW, "low"),
#     ]


# class PrecipDelay:
#     CLEAR = None
#     RAIN = "rain"
#     SNOW = "snow"

#     choices = [
#         (CLEAR, None),
#         (RAIN, "rain"),
#         (SNOW, "snow"),
#     ]
