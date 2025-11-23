from entities.rule_entity import Rule
from repository.rule_repository import RuleRepository


class RuleService:
    def __init__(self, rule_repository: RuleRepository):
        self.rule_repository = rule_repository

    def create_rule(self, rule: Rule):
        return self.rule_repository.create_rule(rule)
