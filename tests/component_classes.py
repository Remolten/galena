from ..galena import galena


@galena.Component
class Health(object):
    health = 1


@galena.Component
class Velocity(object):
    required_components = (Health,)

    speed = 10
    direction = 180


@galena.Component
class Shield(object):
    required_components = (Health, Velocity)

    value = 10
