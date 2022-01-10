import gc
import board
import neopixel
import digitalio

from adafruit_led_animation.color import WHITE, AMBER, RED, BLUE, RAINBOW
from adafruit_led_animation.animation.chase import Chase
# from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.sparkle import Sparkle
# from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.customcolorchase import CustomColorChase

button_pin = digitalio.DigitalInOut(board.A0)
button_pin.direction = digitalio.Direction.INPUT
button_pin.pull = digitalio.Pull.UP
button_state = button_pin.value

pixel_pin = board.A1
pixel_num = 24

pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=0.5, auto_write=False)

# rainbow = Rainbow(pixels, speed=0.1, period=5, step=1, precompute_rainbow=False)
# rainbow.colors = []

mode = -1
animator = None
def updateMode():
    global mode
    global animator
    mode += 1
    if mode > 3:
        mode = 0

    animator = None
    gc.collect()

    if mode == 0:
        animator = CustomColorChase(pixels, speed=0.1, size=6, spacing=1)
    elif mode == 1:
        animator = Sparkle(pixels, speed=0.1, color=WHITE, num_sparkles=3)
    elif mode == 2:
        animator = Chase(pixels, speed=0.1, size=6, spacing=2, color=RED)
    elif mode == 3:
        animator = CustomColorChase(pixels, speed=0.1, size=6, spacing=1, colors=(RED, BLUE))

# Initialize the animator
updateMode()

while True:
    # Check for mode changes as the button is pressed
    state = button_pin.value
    if button_state != state:
        if not button_pin.value:
            updateMode()
        else:
            pass
        button_state = state

    # Keep animating through frames using whatever animator is active
    animator.animate()