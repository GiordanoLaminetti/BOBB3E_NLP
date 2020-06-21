import time
import ev3dev.ev3 as ev3

# set the motor pin
motor_left = ev3.LargeMotor("outC")
motor_right = ev3.LargeMotor("outB")
motor_a = ev3.MediumMotor("outA")
ir = ev3.InfraredSensor()


def straight(**kwargs):
    if 'distance' in kwargs.keys():
        # convert meter in position
        position_sp = kwargs['distance']*60
        motor_left.run_to_rel_pos(
            speed_sp=kwargs['sing']*900, position_sp=position_sp, stop_action='brake')
        motor_right.run_to_rel_pos(
            speed_sp=kwargs['sing']*900, position_sp=position_sp, stop_action='brake')
    elif 'duration' in kwargs.keys():
        # convert time to millisecond
        time_sp = kwargs['duration'] * 1000
        motor_left.run_timed(
            speed_sp=kwargs['sing']*900, time_sp=time_sp, stop_action='brake')
        motor_right.run_timed(
            speed_sp=kwargs['sing']*900, time_sp=time_sp, stop_action='brake')
    else:
        motor_left.run_forever(speed_sp=kwargs['sing']*900)
        motor_right.run_forever(speed_sp=kwargs['sing']*900)


def turn(**kwargs):
    if kwargs['direction'] == 'left':
        rotateLeft()
    elif kwargs['direction'] == 'right':
        rotateRight()
    elif kwargs['direction'] == 'backflip':
        backflip()
    else:
        error()


def rotateLeft():
    motor_left.run_to_rel_pos(
        position_sp=-610, speed_sp=900, stop_action='brake')
    motor_right.run_to_rel_pos(
        position_sp=610, speed_sp=900, stop_action='brake')


def rotateRight():
    motor_left.run_to_rel_pos(
        position_sp=610, speed_sp=900, stop_action='brake')
    motor_right.run_to_rel_pos(
        position_sp=-610, speed_sp=900, stop_action='brake')


def backflip():
    motor_left.run_to_rel_pos(
        position_sp=1250, speed_sp=900, stop_action='brake')
    motor_right.run_to_rel_pos(
        position_sp=-1250, speed_sp=900, stop_action='brake')


def stop(**kwargs):
    motor_left.stop()
    motor_right.stop()


def error():
    ev3.Sound.speak("Sorry i haven't understood",
                    espeak_opts='-a 200 -s 85 -ven+m7').wait()


def hello():
    ev3.Sound.speak("Hello i am ONAR",
                    espeak_opts='-a 200 -s 80 -ven+m7').wait()


def go(**kwargs):
    kwargs['sing'] = -1
    if 'direction' in kwargs.keys():
        if kwargs['direction'] == 'straight':
            straight(**kwargs)
        elif kwargs['direction'] == 'behind':
            kwargs['sing'] = 1
            straight(**kwargs)
        else:
            turn(**kwargs)
            motor_left.wait_until_not_moving()
            straight(**kwargs)


def pick(**kwargs):
    if 'direction' in kwargs.keys():
        go(**kwargs)
        while ir.proximity > 18:
            pass
        stop()
        motor_left.wait_until_not_moving()
    motor_a.run_to_abs_pos(position_sp=400, speed_sp=300)


def put(**kwargs):
    if 'direction' in kwargs.keys():
        go(**kwargs)
        while ir.proximity > 18:
            pass
        stop()
        motor_left.wait_until_not_moving()
    motor_a.run_to_abs_pos(position_sp=-400, speed_sp=300)
