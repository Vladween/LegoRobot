from enum import Enum
from hub import port
import runloop
import motor
import color
import color_sensor
import distance_sensor

class Direction(Enum):
    LEFT = -1
    RIGHT = 1

LeftMotor = port.C
RightMotor = port.D
DistanceSensor = port.E
ColorSensor = port.F

GoVelocity = 500
RotateVelocity = 75
RotateTicks = 6000

LastDirection = Direction.LEFT

def StartStraight(vel: int):
    motor.run(LeftMotor, -vel)
    motor.run(RightMotor, vel) 

def StartLeftTurn(vel: int):
    global LastDirection
    LastDirection = Direction.LEFT
    motor.run(LeftMotor, vel)
    motor.run(RightMotor, vel)

def StartRightTurn(vel: int):
    global LastDirection
    LastDirection = Direction.RIGHT
    motor.run(LeftMotor, -vel)
    motor.run(RightMotor, -vel)

def StartTurn(dir: Direction, vel: int):
    if dir == Direction.LEFT:
        StartLeftTurn(vel)
    else:
        StartRightTurn(vel)

def Stop():
    motor.stop(LeftMotor, stop=motor.CONTINUE)
    motor.stop(RightMotor, stop=motor.CONTINUE)

def RotateForTicksUntil(until: function, ticks: int = RotateTicks, dir: Direction = LastDirection, vel: int = RotateVelocity):
    m_ticks = 0
    while not until():
        StartTurn(dir, vel)
        m_ticks = m_ticks + 1
        if m_ticks >= ticks:
            return

async def SearchUntil(until: function, ticks: int = RotateTicks, dir: Direction = LastDirection, vel: int = RotateVelocity):
    RotateForTicksUntil(until, ticks, dir, vel)
    StartTurn(-dir, vel)
    await runloop.until(until)

def ColorIsBlack():
    return color_sensor.color(ColorSensor) is color.BLACK

def ColorNotBlack():
    return not ColorIsBlack()

def CloserThan(mm: int):
    return distance_sensor.distance(DistanceSensor) <= mm

async def FollowLineUntil(until: function):
    while not until():
        StartStraight(GoVelocity)
        await runloop.until(lambda: ColorNotBlack() or until())
        await SearchUntil(lambda: ColorNotBlack() or until())

async def FollowLine():
    while True:
        StartStraight(GoVelocity)
        await runloop.until(ColorNotBlack)
        await SearchUntil(ColorIsBlack)

runloop.run(FollowLine())