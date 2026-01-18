from gpiozero import MotionSensor

# Connect PIR sensor to GPIO 4 (adjust if needed)
pir = MotionSensor(4)

while True:
    print("No movement found")
    pir.wait_for_motion()

    print("Movement found!")
    pir.wait_for_no_motion()