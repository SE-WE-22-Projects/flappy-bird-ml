from dataclasses import dataclass


@dataclass
class Pipe:
    x: int
    gap_y: int


@dataclass
class Bird:
    y: int
    velocity: float
