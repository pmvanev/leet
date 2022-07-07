import unittest

# Problem: given an hour, minute, and second, find the angle between the hour and minute hands on a clock.
# Notes:
#  - the hour and second hands glide continuously about the clock face.
#  - compute the small angle, answer should be <= 180 deg

minutes_per_hour = 60.
seconds_per_minute = 60.
seconds_per_hour = 3600.
deg_per_minute = 6.
hour_hand_deg_per_hour = 30.
deg_per_revolution = 360


def hour_hand_deg(hour, minute, second):
    deg_per_hour = hour_hand_deg_per_hour
    hour_offset = hour * deg_per_hour
    minute_offset = deg_per_hour * minute / minutes_per_hour
    second_offset = deg_per_hour * second / seconds_per_hour
    return (hour_offset + minute_offset + second_offset) % deg_per_revolution


def minute_hand_deg(minute, second):
    minute_offset = deg_per_minute * minute
    second_offset = deg_per_minute * second / seconds_per_minute
    return (minute_offset + second_offset) % deg_per_revolution


def small_angle_deg(angle_deg):
    _angle_deg = angle_deg % deg_per_revolution
    threshold = deg_per_revolution / 2
    return _angle_deg if _angle_deg <= threshold else deg_per_revolution - _angle_deg


def hand_angle_deg(hour, minute, second):
    hhd = hour_hand_deg(hour, minute, second)
    mhd = minute_hand_deg(minute, second)
    return small_angle_deg(abs(hhd - mhd))


class TestTimeAngle(unittest.TestCase):

    def test_hand_angle_degrees(self):
        self.assertEqual(hand_angle_deg(hour=12, minute=0, second=0), 0)

        time = {'hour': 12, 'minute': 15, 'second': 0}
        _minute_hand_deg = 90
        _hour_hand_deg = (time['minute'] / minutes_per_hour) * hour_hand_deg_per_hour
        self.assertEqual(hand_angle_deg(**time),
                         _minute_hand_deg - _hour_hand_deg)


if __name__ == '__main__':
    unittest.main()