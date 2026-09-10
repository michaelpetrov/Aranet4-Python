# Local changes

Based on upstream 2.6.0. Temperature decoding preserves the sensor's 0.05 °C
steps by dividing the raw integer by 20, after the existing invalid-reading
check. Current readings, advertisements, and history decoding share this
conversion. Pressure, humidity, and terminal display formatting are unchanged.

The one-decimal rounding originated in commit
`696f5b3eefc330a1b81a9ebb9db4688af3beee09` (February 18, 2022), titled
"Round parameter float values to 1 decimal place", in upstream PR #13,
"Refactor". Neither that commit nor its PR discussion explains why temperature
should lose its encoded half-tenth steps. Avoiding floating-point display
artifacts is a possible explanation, not a documented rationale.

Run regression tests with `python -m pytest`.
