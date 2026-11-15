# GENERATED from data/signals.yaml by tools/gen_decoder.py. Do not edit by hand.
#
# MESSAGES maps a CAN id to {"name", "dlc", "signals"}. Each signal is a dict:
#   name, byte, bit (None for whole bytes, else the least significant bit),
#   nbits, endian ("big" or "little"), signed, scale, offset, unit, values
#   (raw -> label, or None), status, alias (True if it reuses the bits of
#   another signal).
# physical value = raw * scale + offset.
MESSAGES = {
    0x205: {
        "name": 'wheel_speeds',
        "dlc": 8,
        "signals": [
            {'name': 'wheel_speed_front', 'byte': 0, 'bit': None, 'nbits': 16, 'endian': 'big', 'signed': False, 'scale': 0.00990099, 'offset': 0, 'unit': 'km/h', 'values': None, 'status': 'confirmed', 'alias': False},
            {'name': 'wheel_speed_rear', 'byte': 2, 'bit': None, 'nbits': 16, 'endian': 'big', 'signed': False, 'scale': 0.00990099, 'offset': 0, 'unit': 'km/h', 'values': None, 'status': 'confirmed', 'alias': False},
            {'name': 'accel_state_bits', 'byte': 5, 'bit': 0, 'nbits': 4, 'endian': 'big', 'signed': False, 'scale': 1, 'offset': 0, 'unit': '', 'values': None, 'status': 'hypothesis', 'alias': False},
            {'name': 'b6b7_always_zero', 'byte': 6, 'bit': None, 'nbits': 16, 'endian': 'big', 'signed': False, 'scale': 1, 'offset': 0, 'unit': '', 'values': None, 'status': 'unknown', 'alias': False},
        ],
    },
    0x209: {
        "name": 'engine_gear',
        "dlc": 6,
        "signals": [
            {'name': 'engine_rpm', 'byte': 0, 'bit': None, 'nbits': 16, 'endian': 'big', 'signed': False, 'scale': 0.390625, 'offset': 0, 'unit': 'rpm', 'values': None, 'status': 'confirmed', 'alias': False},
            {'name': 'b2_unknown', 'byte': 2, 'bit': None, 'nbits': 8, 'endian': 'big', 'signed': False, 'scale': 1, 'offset': 0, 'unit': '', 'values': None, 'status': 'unknown', 'alias': False},
            {'name': 'gear_actual', 'byte': 3, 'bit': 5, 'nbits': 3, 'endian': 'big', 'signed': False, 'scale': 1, 'offset': 0, 'unit': 'gear', 'values': {0: 'neutral', 1: '1st', 2: '2nd', 3: '3rd', 4: '4th', 5: '5th', 6: '6th'}, 'status': 'confirmed', 'alias': False},
            {'name': 'tcs_level', 'byte': 3, 'bit': 1, 'nbits': 4, 'endian': 'big', 'signed': False, 'scale': 1, 'offset': 0, 'unit': '', 'values': {0: 'probably TCS OFF (not confirmed)', 1: 'TCS 1', 2: 'TCS 2', 3: 'TCS M (manual)'}, 'status': 'confirmed', 'alias': False},
            {'name': 'start_flag', 'byte': 3, 'bit': 0, 'nbits': 1, 'endian': 'big', 'signed': False, 'scale': 1, 'offset': 0, 'unit': '', 'values': None, 'status': 'hypothesis', 'alias': False},
            {'name': 'gear_requested', 'byte': 4, 'bit': 0, 'nbits': 3, 'endian': 'big', 'signed': False, 'scale': 1, 'offset': 0, 'unit': 'gear', 'values': {0: 'neutral', 1: '1st', 2: '2nd', 3: '3rd', 4: '4th', 5: '5th', 6: '6th', 7: 'between gears'}, 'status': 'confirmed', 'alias': False},
            {'name': 'b4_bit3_unknown', 'byte': 4, 'bit': 3, 'nbits': 1, 'endian': 'big', 'signed': False, 'scale': 1, 'offset': 0, 'unit': '', 'values': None, 'status': 'unknown', 'alias': False},
            {'name': 'ride_mode', 'byte': 4, 'bit': 6, 'nbits': 2, 'endian': 'big', 'signed': False, 'scale': 1, 'offset': 0, 'unit': '', 'values': {0: 'D-MODE 1', 1: 'D-MODE 2', 2: 'D-MODE 3', 3: 'D-MODE 4'}, 'status': 'confirmed', 'alias': False},
            {'name': 'shift_window_bits', 'byte': 5, 'bit': 2, 'nbits': 2, 'endian': 'big', 'signed': False, 'scale': 1, 'offset': 0, 'unit': '', 'values': {0: 'neither', 1: 'bit 2 only', 2: 'bit 3 only'}, 'status': 'hypothesis', 'alias': False},
        ],
    },
    0x215: {
        "name": 'throttle',
        "dlc": 8,
        "signals": [
            {'name': 'throttle_valve', 'byte': 0, 'bit': None, 'nbits': 16, 'endian': 'big', 'signed': False, 'scale': 1, 'offset': 0, 'unit': 'raw', 'values': None, 'status': 'hypothesis', 'alias': False},
            {'name': 'throttle_grip', 'byte': 2, 'bit': None, 'nbits': 16, 'endian': 'big', 'signed': False, 'scale': 1, 'offset': 0, 'unit': 'raw', 'values': None, 'status': 'confirmed', 'alias': False},
            {'name': 'tcs_level_b4', 'byte': 4, 'bit': 0, 'nbits': 2, 'endian': 'big', 'signed': False, 'scale': 1, 'offset': 0, 'unit': '', 'values': None, 'status': 'confirmed', 'alias': False},
            {'name': 'grip_closed', 'byte': 4, 'bit': 5, 'nbits': 1, 'endian': 'big', 'signed': False, 'scale': 1, 'offset': 0, 'unit': '', 'values': None, 'status': 'confirmed', 'alias': False},
            {'name': 'b4_bits67_unknown', 'byte': 4, 'bit': 6, 'nbits': 2, 'endian': 'big', 'signed': False, 'scale': 1, 'offset': 0, 'unit': '', 'values': None, 'status': 'unknown', 'alias': False},
            {'name': 'tcs_level_b5', 'byte': 5, 'bit': 0, 'nbits': 2, 'endian': 'big', 'signed': False, 'scale': 1, 'offset': 0, 'unit': '', 'values': None, 'status': 'confirmed', 'alias': False},
            {'name': 'tcs_level_b6', 'byte': 6, 'bit': 1, 'nbits': 2, 'endian': 'big', 'signed': False, 'scale': 1, 'offset': 0, 'unit': '', 'values': None, 'status': 'confirmed', 'alias': False},
            {'name': 'ride_mode', 'byte': 7, 'bit': 6, 'nbits': 2, 'endian': 'big', 'signed': False, 'scale': 1, 'offset': 0, 'unit': '', 'values': {0: 'D-MODE 1', 1: 'D-MODE 2', 2: 'D-MODE 3', 3: 'D-MODE 4'}, 'status': 'confirmed', 'alias': False},
        ],
    },
    0x226: {
        "name": 'mode_tcs',
        "dlc": 7,
        "signals": [
            {'name': 'ride_mode', 'byte': 0, 'bit': 6, 'nbits': 2, 'endian': 'big', 'signed': False, 'scale': 1, 'offset': 0, 'unit': '', 'values': {0: 'D-MODE 1', 1: 'D-MODE 2', 2: 'D-MODE 3', 3: 'D-MODE 4'}, 'status': 'confirmed', 'alias': False},
            {'name': 'tcs_pattern', 'byte': 0, 'bit': 0, 'nbits': 4, 'endian': 'big', 'signed': False, 'scale': 1, 'offset': 0, 'unit': '', 'values': {0: 'probably TCS OFF (not confirmed)', 5: 'TCS 1', 10: 'TCS 2', 15: 'TCS M'}, 'status': 'confirmed', 'alias': False},
            {'name': 'tcs_level', 'byte': 3, 'bit': None, 'nbits': 8, 'endian': 'big', 'signed': False, 'scale': 1, 'offset': 0, 'unit': '', 'values': {0: 'probably TCS OFF (not confirmed)', 1: 'TCS 1', 2: 'TCS 2', 3: 'TCS M (manual)'}, 'status': 'confirmed', 'alias': False},
            {'name': 'tcs_level_b5', 'byte': 5, 'bit': 2, 'nbits': 2, 'endian': 'big', 'signed': False, 'scale': 1, 'offset': 0, 'unit': '', 'values': None, 'status': 'confirmed', 'alias': False},
            {'name': 'setting_2bit', 'byte': 5, 'bit': 0, 'nbits': 2, 'endian': 'big', 'signed': False, 'scale': 1, 'offset': 0, 'unit': '', 'values': None, 'status': 'hypothesis', 'alias': False},
        ],
    },
    0x22A: {
        "name": 'brake_switch_candidate',
        "dlc": 2,
        "signals": [
            {'name': 'brake_switch', 'byte': 1, 'bit': 3, 'nbits': 1, 'endian': 'big', 'signed': False, 'scale': 1, 'offset': 0, 'unit': '', 'values': None, 'status': 'hypothesis', 'alias': False},
            {'name': 'b1_motion_flag', 'byte': 1, 'bit': 4, 'nbits': 4, 'endian': 'big', 'signed': False, 'scale': 1, 'offset': 0, 'unit': '', 'values': None, 'status': 'ruled_out', 'alias': True},
        ],
    },
    0x22B: {
        "name": 'unknown_22b',
        "dlc": 2,
        "signals": [
        ],
    },
    0x22E: {
        "name": 'unknown_22e',
        "dlc": 2,
        "signals": [
        ],
    },
    0x23A: {
        "name": 'wake_state',
        "dlc": 3,
        "signals": [
            {'name': 'wake_phase', 'byte': 0, 'bit': None, 'nbits': 8, 'endian': 'big', 'signed': False, 'scale': 1, 'offset': 0, 'unit': '', 'values': {0: 'normal', 4: 'just woken'}, 'status': 'hypothesis', 'alias': False},
        ],
    },
    0x23E: {
        "name": 'temperatures',
        "dlc": 4,
        "signals": [
            {'name': 'coolant_temp', 'byte': 0, 'bit': None, 'nbits': 8, 'endian': 'big', 'signed': False, 'scale': 0.625, 'offset': -30, 'unit': 'degC', 'values': None, 'status': 'confirmed', 'alias': False},
            {'name': 'air_temp', 'byte': 1, 'bit': None, 'nbits': 8, 'endian': 'big', 'signed': False, 'scale': 1, 'offset': -55, 'unit': 'degC', 'values': None, 'status': 'hypothesis', 'alias': False},
            {'name': 'load_counter', 'byte': 2, 'bit': None, 'nbits': 16, 'endian': 'big', 'signed': False, 'scale': 1, 'offset': 0, 'unit': 'raw', 'values': None, 'status': 'hypothesis', 'alias': False},
        ],
    },
    0x245: {
        "name": 'unknown_245',
        "dlc": 1,
        "signals": [
        ],
    },
    0x250: {
        "name": 'imu_accel',
        "dlc": 8,
        "signals": [
            {'name': 'accel_x', 'byte': 0, 'bit': None, 'nbits': 16, 'endian': 'big', 'signed': False, 'scale': 0.001008, 'offset': -7.056, 'unit': 'g', 'values': None, 'status': 'confirmed', 'alias': False},
            {'name': 'accel_y', 'byte': 2, 'bit': None, 'nbits': 16, 'endian': 'big', 'signed': False, 'scale': 0.001008, 'offset': -7.056, 'unit': 'g', 'values': None, 'status': 'confirmed', 'alias': False},
            {'name': 'accel_z', 'byte': 4, 'bit': None, 'nbits': 16, 'endian': 'big', 'signed': False, 'scale': 0.001008, 'offset': -7.056, 'unit': 'g', 'values': None, 'status': 'confirmed', 'alias': False},
            {'name': 'lean_static', 'byte': 2, 'bit': None, 'nbits': 16, 'endian': 'big', 'signed': False, 'scale': -0.057412, 'offset': 402.59, 'unit': 'deg', 'values': None, 'status': 'confirmed', 'alias': True},
            {'name': 'power_up_flags', 'byte': 6, 'bit': None, 'nbits': 8, 'endian': 'big', 'signed': False, 'scale': 1, 'offset': 0, 'unit': '', 'values': {32: 'normal', 96: 'first 0.4 s after power-up', 128: 'first frame'}, 'status': 'hypothesis', 'alias': False},
        ],
    },
    0x254: {
        "name": 'imu_gyro',
        "dlc": 8,
        "signals": [
            {'name': 'roll_rate', 'byte': 0, 'bit': None, 'nbits': 16, 'endian': 'big', 'signed': False, 'scale': 0.01, 'offset': -300, 'unit': 'deg/s', 'values': None, 'status': 'confirmed', 'alias': False},
            {'name': 'pitch_rate', 'byte': 2, 'bit': None, 'nbits': 16, 'endian': 'big', 'signed': False, 'scale': 0.01, 'offset': -300, 'unit': 'deg/s', 'values': None, 'status': 'hypothesis', 'alias': False},
            {'name': 'yaw_rate', 'byte': 4, 'bit': None, 'nbits': 16, 'endian': 'big', 'signed': False, 'scale': 0.01, 'offset': -300, 'unit': 'deg/s', 'values': None, 'status': 'confirmed', 'alias': False},
            {'name': 'b6_unknown', 'byte': 6, 'bit': None, 'nbits': 8, 'endian': 'big', 'signed': False, 'scale': 1, 'offset': 0, 'unit': '', 'values': None, 'status': 'unknown', 'alias': False},
        ],
    },
    0x258: {
        "name": 'imu_derived',
        "dlc": 8,
        "signals": [
            {'name': 'b0b3_unknown', 'byte': 0, 'bit': None, 'nbits': 32, 'endian': 'big', 'signed': False, 'scale': 1, 'offset': 0, 'unit': '', 'values': None, 'status': 'unknown', 'alias': False},
            {'name': 'b4b5_always_zero', 'byte': 4, 'bit': None, 'nbits': 16, 'endian': 'big', 'signed': False, 'scale': 1, 'offset': 0, 'unit': '', 'values': None, 'status': 'unknown', 'alias': False},
            {'name': 'pitch_rate_level', 'byte': 6, 'bit': None, 'nbits': 16, 'endian': 'big', 'signed': False, 'scale': 0.01, 'offset': -300, 'unit': 'deg/s', 'values': None, 'status': 'hypothesis', 'alias': False},
        ],
    },
    0x25C: {
        "name": 'imu_unknown',
        "dlc": 4,
        "signals": [
        ],
    },
    0x260: {
        "name": 'brake_pressure',
        "dlc": 8,
        "signals": [
            {'name': 'brake_pressure_front', 'byte': 0, 'bit': None, 'nbits': 16, 'endian': 'big', 'signed': False, 'scale': 1, 'offset': 0, 'unit': 'raw', 'values': None, 'status': 'confirmed', 'alias': False},
        ],
    },
    0x268: {
        "name": 'abs_status',
        "dlc": 6,
        "signals": [
            {'name': 'not_moved_since_start', 'byte': 1, 'bit': 0, 'nbits': 1, 'endian': 'big', 'signed': False, 'scale': 1, 'offset': 0, 'unit': '', 'values': None, 'status': 'hypothesis', 'alias': False},
            {'name': 'vehicle_speed', 'byte': 2, 'bit': None, 'nbits': 16, 'endian': 'big', 'signed': False, 'scale': 0.056497, 'offset': 0, 'unit': 'km/h', 'values': None, 'status': 'confirmed', 'alias': False},
            {'name': 'abs_rear_active', 'byte': 4, 'bit': 0, 'nbits': 1, 'endian': 'big', 'signed': False, 'scale': 1, 'offset': 0, 'unit': '', 'values': None, 'status': 'confirmed', 'alias': False},
            {'name': 'abs_front_active', 'byte': 4, 'bit': 1, 'nbits': 1, 'endian': 'big', 'signed': False, 'scale': 1, 'offset': 0, 'unit': '', 'values': None, 'status': 'confirmed', 'alias': False},
            {'name': 'rear_brake_pedal', 'byte': 4, 'bit': 2, 'nbits': 1, 'endian': 'big', 'signed': False, 'scale': 1, 'offset': 0, 'unit': '', 'values': None, 'status': 'confirmed', 'alias': False},
            {'name': 'setting_2bit', 'byte': 4, 'bit': 3, 'nbits': 2, 'endian': 'big', 'signed': False, 'scale': 1, 'offset': 0, 'unit': '', 'values': None, 'status': 'hypothesis', 'alias': False},
        ],
    },
    0x401: {
        "name": 'shutdown_state',
        "dlc": 1,
        "signals": [
            {'name': 'after_run', 'byte': 0, 'bit': 7, 'nbits': 1, 'endian': 'big', 'signed': False, 'scale': 1, 'offset': 0, 'unit': '', 'values': None, 'status': 'hypothesis', 'alias': False},
        ],
    },
    0x590: {
        "name": 'unknown_590',
        "dlc": 4,
        "signals": [
        ],
    },
}
