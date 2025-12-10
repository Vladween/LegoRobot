from hub import port
import runloop
import motor
import color
import color_sensor

LeftMotor = port.C
RightMotor = port.D
ColorSensor = port.F
MaxVelocity = 500
MinVelocity = 75
RotateTicks = 6000

def GoStraight(vel: int):
    motor.run(LeftMotor, -vel)
    motor.run(RightMotor, vel) 

def TurnLeft(vel: int):
    motor.run(LeftMotor, vel)
    motor.run(RightMotor, vel)

def TurnRight(vel: int):
    motor.run(LeftMotor, -vel)
    motor.run(RightMotor, -vel)

def TurnSameDir(vel: int):
    if direction == 1:
        TurnLeft(vel)
    else:
        TurnRight(vel)

def Stop():
    motor.stop(LeftMotor, stop=motor.CONTINUE)
    motor.stop(RightMotor, stop=motor.CONTINUE)

def ColorIsBlack():
    return color_sensor.color(ColorSensor) is color.BLACK

def ColorNotBlack():
    return not ColorIsBlack()

direction = 1

async def Search():
    global direction

    fullsearch = False
    ticks = 0

    while ColorNotBlack():
        TurnSameDir(MinVelocity)
        if not fullsearch:        
            ticks = ticks + 1
            if ticks >= RotateTicks:
                direction = -direction
                fullsearch = True

async def main():
    global direction 

    while True:
        GoStraight(MaxVelocity)
        await runloop.until(ColorNotBlack)
        await Search()

runloop.run(main())