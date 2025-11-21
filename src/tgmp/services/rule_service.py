from entities.rule_entity import Rule
from repository.rule_repository import RuleRepository


class RuleService:

    @staticmethod
    def create_rule(rule: Rule):
        return RuleRepository.create_rule(rule)
