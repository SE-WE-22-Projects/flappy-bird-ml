from dataclasses import dataclass


@dataclass
class Pipe:
    x: int
    gap_y: int
    gap_size: int


@dataclass
class GameState:
    bird_y: int
    bird_velocity: float

    pipes: list[Pipe]
