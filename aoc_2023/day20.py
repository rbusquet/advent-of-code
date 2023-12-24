from __future__ import annotations

import abc
import argparse
import enum
import sys
from collections import deque
from dataclasses import dataclass, field
from math import lcm
from typing import Iterator, TextIO


@dataclass
class Arguments:
    file: TextIO = sys.stdin


def strip_lines(file: TextIO) -> Iterator[str]:
    for line in file:
        yield line.strip()


class Pulse(enum.Flag):
    LOW = 0
    HIGH = 1


@dataclass
class Module(abc.ABC):
    name: str
    outputs: list["Module"] = field(default_factory=list)

    @abc.abstractmethod
    def process(self, event: Event, bus: Bus) -> None:
        raise NotImplementedError

    @classmethod
    def from_str(cls, source: str) -> Module:
        if source[0] == "%":
            return FlipFlop(source[1:])
        elif source[0] == "&":
            return Conjunction(source[1:])
        elif source == "broadcaster":
            return Broadcaster(source)
        else:
            return Unknown(source)


@dataclass
class Event:
    pulse: Pulse
    sender: Module
    receiver: Module
    sub_circuit: Module | None = None

    def __repr__(self) -> str:
        # return f"Event({self.pulse.name}, {self.sender.name}, {self.receiver.name})"
        return f"{self.sender.name} -{self.pulse.name}-> {self.receiver.name}"


class Bus(deque[Event]):
    ...


@dataclass
class FlipFlop(Module):
    state: Pulse = Pulse.LOW

    def process(self, event: Event, bus: Bus) -> None:
        if event.pulse == Pulse.HIGH:
            return
        self.state = ~self.state
        for output in self.outputs:
            bus.append(Event(self.state, self, output))

    def __repr__(self) -> str:
        return f'FlipFlop("{self.name}", {self.state})'

    def __hash__(self) -> int:
        return hash((self.name, self.state))


@dataclass
class Conjunction(Module):
    memory: dict[str, Pulse] = field(default_factory=dict)

    @property
    def state(self) -> Pulse:
        if all(value == Pulse.HIGH for value in self.memory.values()):
            return Pulse.LOW
        return Pulse.HIGH

    def process(self, event: Event, bus: Bus) -> None:
        self.memory[event.sender.name] = event.pulse
        for output in self.outputs:
            bus.append(Event(self.state, self, output))

    def __repr__(self) -> str:
        return f'Conjunction("{self.name}", {self.state})'

    def __hash__(self) -> int:
        return hash((self.name, *sorted(self.memory.items())))


@dataclass
class Broadcaster(Module):
    def process(self, event: Event, bus: Bus) -> None:
        for output in self.outputs:
            if event.sub_circuit and output != event.sub_circuit:
                continue
            bus.append(Event(event.pulse, self, output))

    def __repr__(self) -> str:
        return "Broadcaster()"


@dataclass
class Button(Module):
    def process(self, event: Event, bus: Bus) -> None:
        ...

    def press(self, circuit: Module | None = None) -> list[Event]:
        bus = Bus()
        for output in self.outputs:
            bus.append(Event(Pulse.LOW, self, output, sub_circuit=circuit))

        processed_events = []
        while bus:
            event = bus.popleft()
            processed_events.append(event)
            event.receiver.process(event, bus)
        return processed_events


class Unknown(Module):
    state: Pulse | None = None

    def process(self, event: Event, bus: Bus) -> None:
        self.state = event.pulse

    def __repr__(self) -> str:
        return f'Unknown("{self.name}" {self.state})'


def part_1(file: TextIO) -> int:
    file.seek(0)

    outputs = dict[str, list[str]]()
    modules = dict[str, Module]()

    for line in strip_lines(file):
        source, outs = line.split(" -> ")
        if source[0] == "%":
            source = source[1:]
            modules[source] = FlipFlop(source)
        elif source[0] == "&":
            source = source[1:]
            modules[source] = Conjunction(source)
        elif source == "broadcaster":
            modules[source] = Broadcaster(source)
        else:
            modules[source] = Unknown(source)

        outputs[source] = outs.split(", ")

    for source, output_names in outputs.items():
        for out in output_names:
            if out not in modules:
                modules[out] = Unknown(out)
            out_module = modules[out]

            modules[source].outputs.append(out_module)
            if isinstance(out_module, Conjunction):
                out_module.memory[source] = Pulse.LOW

    button = Button("button")
    button.outputs.append(modules["broadcaster"])

    hi_count = 0
    lo_count = 0
    for _ in range(1000):
        events = button.press()
        for event in events:
            if event.pulse == Pulse.HIGH:
                hi_count += 1
            else:
                lo_count += 1

    return hi_count * lo_count


def part_2(file: TextIO) -> int:
    file.seek(0)

    outputs = dict[str, list[str]]()
    modules = dict[str, Module]()

    for line in strip_lines(file):
        source, outs = line.split(" -> ")
        if source[0] == "%":
            source = source[1:]
            modules[source] = FlipFlop(source)
        elif source[0] == "&":
            source = source[1:]
            modules[source] = Conjunction(source)
        elif source == "broadcaster":
            modules[source] = Broadcaster(source)
        else:
            modules[source] = Unknown(source)

        outputs[source] = outs.split(", ")

    for source, output_names in outputs.items():
        for out in output_names:
            if out not in modules:
                modules[out] = Unknown(out)
            out_module = modules[out]

            modules[source].outputs.append(out_module)
            if isinstance(out_module, Conjunction):
                out_module.memory[source] = Pulse.LOW

    button = Button("button")
    button.outputs.append(modules["broadcaster"])

    rx = modules["rx"]
    assert isinstance(rx, Unknown)
    sub_circuits = modules["broadcaster"].outputs

    counts = [0] * len(sub_circuits)
    for i, circuit in enumerate(sub_circuits):
        initial_state = tuple(
            [
                hash(module)
                for module in modules.values()
                if isinstance(module, FlipFlop)
            ]
        )

        while True:
            counts[i] += 1
            button.press(circuit)
            state = tuple(
                [
                    hash(module)
                    for module in modules.values()
                    if isinstance(module, FlipFlop)
                ]
            )
            if state == initial_state:
                break

            if rx.state == Pulse.LOW:
                break

    return lcm(*counts)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=argparse.FileType("r"))
    args = Arguments()
    parser.parse_args(namespace=args)
    print(part_1(args.file))
    print(part_2(args.file))
