class Mapper:
    def __init__(self):
        self.config = {
            "steering_sens": 1.2,
            "steering_curve": 0.8,
            "deadzone": 0.03,
            "invert_steering": False,

            "throttle_curve": 1.5,
            "brake_curve": 1.5,
            "invert_throttle": False,
            "invert_brake": False,
        }

    def map_steering(self, val: float) -> int:
        if abs(val) < self.config["deadzone"]:
            return 0

        val *= self.config["steering_sens"]
        val = max(-1.0, min(1.0, val))

        if val != 0:
            val = (abs(val) ** self.config["steering_curve"]) * (1 if val > 0 else -1)

        if self.config["invert_steering"]:
            val *= -1

        return int(val * 32767)

    def map_trigger(self, val: float, mode: str) -> int:
        val = max(0.0, min(1.0, val))

        if mode == "throttle":
            val = val ** self.config["throttle_curve"]
            if self.config["invert_throttle"]:
                val = 1 - val

        elif mode == "brake":
            val = val ** self.config["brake_curve"]
            if self.config["invert_brake"]:
                val = 1 - val

        return int(val * 255)