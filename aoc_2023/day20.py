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

    @property
    def on(self) -> bool:
        return self.state == Pulse.HIGH

    @property
    def off(self) -> bool:
        return self.state == Pulse.LOW

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


def process_input(file: TextIO):
    outputs = dict[str, list[str]]()
    modules = dict[str, Module]()
    flip_flops = list[FlipFlop]()
    for line in strip_lines(file):
        source, outs = line.split(" -> ")
        if source[0] == "%":
            source = source[1:]
            ff = FlipFlop(source)
            flip_flops.append(ff)
            modules[source] = ff
        elif source[0] == "&":
            source = source[1:]
            modules[source] = Conjunction(source)
        elif source == "broadcaster":
            modules[source] = Broadcaster(source)

        outputs[source] = outs.split(", ")

    for source, output_names in outputs.items():
        for out in output_names:
            if out not in modules:
                continue
            out_module = modules[out]

            modules[source].outputs.append(out_module)
            if isinstance(out_module, Conjunction):
                out_module.memory[source] = Pulse.LOW

    return modules, flip_flops


def part_1(file: TextIO) -> int:
    file.seek(0)

    modules, flip_flops = process_input(file)

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

    modules, flip_flops = process_input(file)

    button = Button("button")
    button.outputs.append(modules["broadcaster"])

    sub_circuits = modules["broadcaster"].outputs

    counts = [0] * len(sub_circuits)
    for i, circuit in enumerate(sub_circuits):
        while True:
            counts[i] += 1
            button.press(circuit)
            all_off = all(ff.off for ff in flip_flops)

            if all_off:  # looped back to start
                break

    # this output is how many presses it takes to get all flip flops to be off
    # I don't really understand why this works, but it does
    return lcm(*counts)


def part_2_looking_at_outputs(file: TextIO) -> int:
    file.seek(0)

    modules, flip_flops = process_input(file)

    button = Button("button")
    button.outputs.append(modules["broadcaster"])

    # conjunction vf outputs to output rx
    # hf, pk, mk, pm are conjunctions and output to vf
    # if we count how many times we have to press the button
    # to get these conjunctions to output a high pulse,
    # we can find the least common multiple of these counts
    # and that will be the number of times we have to press the button
    # to get a low pulse from vf
    important_conjunctions = ["hf", "pk", "mk", "pm"]

    counts = []
    count = 0
    while True:
        count += 1
        events = button.press()
        conjunction_events = [
            e for e in events if e.sender.name in important_conjunctions
        ]
        for event in conjunction_events:
            if event.pulse == Pulse.HIGH:
                counts.append(count)
                important_conjunctions.remove(event.sender.name)
                if not important_conjunctions:
                    return lcm(*counts)

    # this output is how many presses it takes to get all flip flops to be off
    # I don't really understand why this works, but it does
    return lcm(*counts)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=argparse.FileType("r"))
    args = Arguments()
    parser.parse_args(namespace=args)
    print(part_1(args.file))
    print(part_2(args.file))
    print(part_2_looking_at_outputs(args.file))
