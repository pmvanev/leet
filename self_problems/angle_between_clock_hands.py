import unittest

# Problem: given an hour, minute, and second, find the angle between the hour and minute hands on a clock.
# Notes:
#  - the hour and second hands glide continuously about the clock face.
#  - compute the small angle, answer should be <= 180 deg

minutes_per_hour = 60.
seconds_per_minute = 60.
seconds_per_hour = 3600.
deg_per_minute = 6.
deg_per_revolution = 360.
hours_per_revolution = 12.
minutes_per_revolution = 60.
seconds_per_revolution = 60.


def hour_hand_deg(hour, minute, second):
    deg_per_hour = 30.
    hour_offset = hour * deg_per_hour
    minute_offset = deg_per_hour * minute / minutes_per_hour
    second_offset = deg_per_minute * second / seconds_per_hour
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
    _hour = hour % hours_per_revolution
    _minute = minute % minutes_per_revolution
    _second = second % seconds_per_revolution
    hhd = hour_hand_deg(_hour, _minute, _second)
    mhd = minute_hand_deg(_minute, _second)
    return small_angle_deg(abs(hhd - mhd))


class TestTimeAngle(unittest.TestCase):

    def test_hand_angle_degrees(self):
        time = {'hour': 0, 'minute': 0, 'second': 0}
        self.assertEqual(hand_angle_deg(**time), 0)

        time = {'hour': 12, 'minute': 15, 'second': 0}
        # 15 min is .25 hour, so the hour hand should be at .25*30d
        self.assertEqual(hand_angle_deg(**time), 90 - .25 * 30)

        time = {'hour': 3, 'minute': 15, 'second': 0}
        # 15 min is .25 hour, so the hour hand should be .25*30d past minute hand
        self.assertEqual(hand_angle_deg(**time), .25 * 30)

        time = {'hour': 6, 'minute': 30, 'second': 0}
        # 30 min is .5 hour, so the hour hand should be .5*30d past minute hand
        self.assertEqual(hand_angle_deg(**time), .5 * 30)

        time = {'hour': 6, 'minute': 45, 'second': 0}
        # 30 min is .5 hour, so the hour hand should be .75*30d past 6
        self.assertEqual(hand_angle_deg(**time), 270 - (180 + .75 * 30))

        time = {'hour': 11, 'minute': 59, 'second': 0}
        # minute hand: 59/60 * 360
        m = 59 / 60 * 360
        h = (11 + 59 / 60) * 30
        self.assertEqual(hand_angle_deg(**time), h - m)

        time = {'hour': 12, 'minute': 00, 'second': 59}
        m = 59 / 60 * 6
        h = m / 60
        self.assertAlmostEqual(hand_angle_deg(**time), m - h)


if __name__ == '__main__':
    unittest.main()