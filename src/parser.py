from __future__ import annotations
from typing import Optional

class ASTNode():
    pass

class Program(ASTNode):
    
    def __init__(self, children: list[Rule] = []) -> None:
        self.rootNode: Program = self
        self.children: list[Rule] = children

class Rule(ASTNode):
    
    def __init__(self, root: Optional[Program] = None, 
                 children: list[tuple[Condition, Command]] = []) -> None:
        self.rootNode: Optional[Program] = root 
        self.children: list[tuple[Condition, Command]] = children

class Condition(ASTNode):
    pass

class Command(ASTNode):

    def __init__(self, root: Optional[Program] = None, children: Optional[Update | UpdateOrAction] = None) -> None:
        self.root: Optional[Program] = root
        self.children: Optional[Update | UpdateOrAction] = children

class Update(ASTNode):
    pass

class UpdateOrAction(ASTNode):
    pass




