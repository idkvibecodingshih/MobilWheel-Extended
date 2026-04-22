import vgamepad as vg
import logging

class VJoyController:
    def __init__(self):
        self.gamepad = vg.VX360Gamepad()
        logging.info("Controle virtual criado")

    def update_all(self, steer, throttle, brake):
        self.gamepad.left_joystick(x_value=steer, y_value=0)
        self.gamepad.right_trigger(value=throttle)
        self.gamepad.left_trigger(value=brake)
        self.gamepad.update()

    def press_button(self, btn):
        mapping = {
            "x": vg.XUSB_BUTTON.XUSB_GAMEPAD_X,
            "y": vg.XUSB_BUTTON.XUSB_GAMEPAD_Y,
            "lb": vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER,
            "rb": vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER,
            "handbrake": vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB,
            "boost": vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB,
        }

        if btn in mapping:
            self.gamepad.press_button(mapping[btn])
            self.gamepad.update()

    def release_button(self, btn):
        mapping = {
            "x": vg.XUSB_BUTTON.XUSB_GAMEPAD_X,
            "y": vg.XUSB_BUTTON.XUSB_GAMEPAD_Y,
            "lb": vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER,
            "rb": vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER,
            "handbrake": vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB,
            "boost": vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB,
        }

        if btn in mapping:
            self.gamepad.release_button(mapping[btn])
            self.gamepad.update()

    def reset(self):
        self.gamepad.reset()
        self.gamepad.update()