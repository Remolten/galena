import pytest

from ..galena import galena


@pytest.fixture
def game():
    yield galena.Game()


@pytest.fixture
def entity(game):
    yield game.create_entity()


@pytest.fixture
def entity2(game):
    yield game.create_entity()


@pytest.fixture
def entity3(game):
    yield game.create_entity()
