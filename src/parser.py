from __future__ import annotations
from typing import Optional, ClassVar, Iterable

class ASTNode():
    _children: ClassVar[tuple[str, ...]] = ()
    
    def __iter__(self) -> Iterable[ASTNode]:
        for fieldName in self._children:
            value = getattr(self, fieldName, None)
            if isinstance(value, list):
                yield from (item for item in value 
                            if isinstance(item, ASTNode))
            elif isinstance(value, ASTNode):
                yield value

    
class Program(ASTNode):
    _children: ClassVar[tuple[str]] = ('rules',)

    def __init__(self, rules: list[Rule] = []) -> None:
        self.rules: list[Rule] = rules

    def addRule(self, rule: Rule|None = None, condition: Condition|None = None, command: Command|None = None) -> None:
        if rule is not None and (condition is None and command is None):
            self.rules.append(rule)
        elif rule is None and (condition is not None and command is not None):
            self.rules.append(Rule(condition=condition, command=command))
        else:
            raise ValueError('Invalid arguments: Provide either a "rule" or both a "condition" and a "command".')
        


class Rule(ASTNode):
    _children: ClassVar[tuple[str, str]] = ('condition', 'command')
    
    def __init__(self, condition: Optional[Condition] = None, command: Optional[Command] = None) -> None:
        self.condition = condition
        self.command = command

    def setRule(self, condition: Condition, command: Command) -> None: 
        self.condition = condition
        self.command = command


class Condition(ASTNode):
    pass


class Command(ASTNode):
    _children: ClassVar[tuple[str, str]] = ('updates', 'action')

    def __init__(self) -> None:
        self.updates: list[Update] = []
        self.action: Action = Action()


class Update(ASTNode):
    pass


class Action(ASTNode):
    pass


class Relation(ASTNode):

    def __init__(self, root: Optional[Program] = None) -> None:
        pass


