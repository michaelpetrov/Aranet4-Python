"""Preserve encoded resolution in both current and historical measurements."""

import unittest

from aranet4.client import AranetType, CurrentReading, Param


class TemperaturePrecisionTests(unittest.TestCase):
    """Exercise odd raw values that used to lose half-tenth degree steps."""

    def test_temperature_steps(self) -> None:
        for raw, expected in (
            (0, 0.0),
            (1, 0.05),
            (415, 20.75),
            (417, 20.85),
            (481, 24.05),
            (483, 24.15),
            (1000, 50.0),
        ):
            with self.subTest(raw=raw):
                self.assertEqual(CurrentReading._set(Param.TEMPERATURE, raw), expected)

    def test_current_reading_preserves_resolution(self) -> None:
        reading = CurrentReading()
        reading.decode((600, 481, 10132, 50, 100, 1, 60, 3), AranetType.ARANET4)
        self.assertEqual(reading.temperature, 24.05)
        self.assertEqual(reading.pressure, 1013.2)

    def test_invalid_temperature_still_returns_sentinel(self) -> None:
        self.assertEqual(CurrentReading._set(Param.TEMPERATURE, 0x4000), -1)

    def test_other_measurements_keep_their_resolution(self) -> None:
        self.assertEqual(CurrentReading._set(Param.PRESSURE, 10123), 1012.3)
        self.assertEqual(CurrentReading._set(Param.HUMIDITY2, 523), 52.3)
        self.assertEqual(CurrentReading._set(Param.CO2, 603), 603)


if __name__ == "__main__":
    unittest.main()
