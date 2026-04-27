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
    _children: ClassVar[tuple[str, ...]] = ('rules',)

    
    def __init__(self, rules: list[Rule] = []) -> None:
        self.rules: list[Rule] = rules

class Rule(ASTNode):
    
    def __init__(self, root: Optional[Program] = None, 
                 children: list[tuple[Condition, Command]] = []) -> None:
        self.rootNode: Optional[Program] = root 
        self.children: list[tuple[Condition, Command]] = children

class Condition(ASTNode):
    pass

class Command(ASTNode):

    def __init__(self, root: Optional[Program] = None, 
                 children: Optional[Update | UpdateOrAction] = None) -> None:
        self.root: Optional[Program] = root
        self.children: Optional[Update | UpdateOrAction] = children

class Update(ASTNode):
    pass

class UpdateOrAction(ASTNode):
    pass

class Relation(ASTNode):

    def __init__(self, root: Optional[Program] = None) -> None:
        pass


