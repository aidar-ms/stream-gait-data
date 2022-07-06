from typing import Union


class Surface:
    # Calibration
    CALIB = 1
    # Flat Even
    FE = 2
    # Cobblestone
    CS = 3
    # Stairs Up
    STR_U = 4
    # Stairs Down
    STR_D = 5
    # Slope Up
    SLP_U = 6
    # Slope Down
    SLP_D = 7
    # Bank Left
    BNK_L = 8
    # Bank Right
    BNK_R = 9
    # G
    GR = 10

    CODES = {
        (1, 2, 3): CALIB,
        (4, 5, 6, 7, 8, 9): FE,
        (10, 11, 12, 13, 14, 15): CS,
        (16, 18, 20, 22, 24, 26): STR_U,
        (17, 19, 21, 23, 25, 27): STR_D,
        (28, 30, 32, 34, 36, 38): SLP_U,
        (29, 31, 33, 35, 37, 39): SLP_D,
        (40, 42, 44, 46, 48, 50): BNK_L,
        (41, 43, 45, 47, 49, 51): BNK_R,
        (52, 53, 54, 55, 56, 57): GR,
    }

    @classmethod
    def get_code(cls, surface_number: Union[int, str]) -> str:

        if isinstance(surface_number, str):
            surface_number = int(surface_number)

        for bucket in cls.CODES:
            # NOTE: Linear search will do just fine...
            if binary_search_bucket(surface_number, bucket) is not None:
                return cls.CODES[bucket]


def binary_search_bucket(n, bucket):
    l, r = 0, len(bucket) - 1
    while l <= r:
        m = l + (r - l) // 2
        if n < bucket[m]:
            r = m - 1
        elif n > bucket[m]:
            l = m + 1
        else:
            return bucket[m]
