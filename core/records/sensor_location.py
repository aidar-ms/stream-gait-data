

class SensorLocation:
    TRUNK = 1
    WRIST = 2
    RIGHT_THIGH = 3
    LEFT_THIGH = 4
    RIGHT_SHANK = 5
    LEFT_SHANK = 6

    # Mapping from original alphanumeric codes to local constants
    CODES = {
        "CC": TRUNK,
        "95": WRIST,
        "93": RIGHT_THIGH,
        "8B": LEFT_THIGH,
        "9B": RIGHT_SHANK,
        "B6": LEFT_SHANK
    }

    # Mapping from local constants to human-readable values
    HUMAN_READABLES = {
        TRUNK: "Trunk",
        WRIST: "Wrist",
        RIGHT_THIGH: "Right Thigh",
        LEFT_THIGH: "Left Thigh",
        RIGHT_SHANK: "Right Shank",
        LEFT_SHANK: "Left Shank"
    }

    @classmethod
    def get_code(cls, number: str) -> int:
        return cls.CODES[number]
