import pytest

import galena


@pytest.fixture
def game():
    return galena.Game()


@pytest.fixture
def entity(game):
    return game.create_entity()


@pytest.fixture
def entity2(game):
    return game.create_entity()


@pytest.fixture
def entity3(game):
    return game.create_entity()
