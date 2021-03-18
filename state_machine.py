import random
import math
from constants import *
from random import uniform, randint


class FiniteStateMachine(object):
    """
    A finite state machine.
    """

    def __init__(self, state):
        self.state = state

    def change_state(self, new_state):
        self.state = new_state

    def update(self, agent):
        self.state.check_transition(agent, self)
        self.state.execute(agent)


class State(object):
    """
    Abstract state class.
    """

    def __init__(self, state_name):
        """
        Creates a state.

        :param state_name: the name of the state.
        :type state_name: str
        """
        self.state_name = state_name

    def check_transition(self, agent, fsm):
        """
        Checks conditions and execute a state transition if needed.

        :param agent: the agent where this state is being executed on.
        :param fsm: finite state machine associated to this state.
        """
        raise NotImplementedError("This method is abstract and must be implemented in derived classes")

    def execute(self, agent):
        """
        Executes the state logic.

        :param agent: the agent where this state is being executed on.
        """
        raise NotImplementedError("This method is abstract and must be implemented in derived classes")


class MoveForwardState(State):
    def __init__(self):
        super().__init__("MoveForward")
        # Todo: add initialization code
        self.t = 0.0
        self.n = 0

    def check_transition(self, agent, state_machine):
        # Todo: add logic to check and execute state transition
        if agent.get_bumper_state():
            state_machine.change_state(GoBackState())
        if self.t > MOVE_FORWARD_TIME:
            state_machine.change_state(MoveInSpiralState())
        pass

    def execute(self, agent):
        # Todo: add execution logic
        self.t = self.n * SAMPLE_TIME
        print("Tempo em frente = {:.2f} segundos".format(self.t))
        agent.set_velocity(FORWARD_SPEED, 0.0)
        self.n += 1
        pass


class MoveInSpiralState(State):
    def __init__(self):
        super().__init__("MoveInSpiral")
        # Todo: add initialization code
        self.n = 0
        self.t = 0.0

    def check_transition(self, agent, state_machine):
        # Todo: add logic to check and execute state transition
        if agent.get_bumper_state():
            state_machine.change_state(GoBackState())
        if self.t > MOVE_IN_SPIRAL_TIME:
            state_machine.change_state(MoveForwardState())
        pass

    def execute(self, agent):
        # Todo: add execution logic
        self.t = self.n * SAMPLE_TIME
        r = INITIAL_RADIUS_SPIRAL + SPIRAL_FACTOR * self.t
        w = FORWARD_SPEED/r
        agent.set_velocity(FORWARD_SPEED, w)
        self.n += 1
        print("Tempo em espiral= {:.2f} segundos".format(self.t))
        pass


class GoBackState(State):
    def __init__(self):
        super().__init__("GoBack")
        # Todo: add initialization code
        self.n = 0

    def check_transition(self, agent, state_machine):
        # Todo: add logic to check and execute state transition
        if self.n > (GO_BACK_TIME/SAMPLE_TIME):
            state_machine.change_state(RotateState())
        pass

    def execute(self, agent):
        # Todo: add execution logic
        agent.set_velocity(BACKWARD_SPEED, 0.0)
        self.n += 1
        pass


class RotateState(State):
    def __init__(self):
        super().__init__("Rotate")
        # Todo: add initialization code
        self.t = 0.0
        self.n = 0.0
        self.s = randint(-1, 1) # Sinal aleatório para mudar o sentido do angulo
        if self.s == 0:
            self.s = 1

    def check_transition(self, agent, state_machine):
        # Todo: add logic to check and execute state transition
        if self.t > 2.0:
            state_machine.change_state(MoveForwardState())
        pass

    def execute(self, agent):
        # Todo: add execution logic
        self.t = self.n * SAMPLE_TIME
        agent.set_velocity(0.0, self.s*ANGULAR_SPEED)
        self.n += 1
        print("Tempo Rotacionando = {:.2f} segundos".format(self.t))
        pass
