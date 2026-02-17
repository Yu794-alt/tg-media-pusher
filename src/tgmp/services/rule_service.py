from entities.rule_entity import Rule
from entities.user_entity import User
from repository.rule_repository import RuleRepository


class RuleService:

    def __init__(self, rule_repository: RuleRepository):
        self.rule_repository = rule_repository

    def create_rule(self, rule: Rule):
        return self.rule_repository.create_rule(rule)

    def find_rule_by_user(self, user: User):
        return self.rule_repository.find_rule_by_user(user)

    def find_all_rules_by_user(self, user: User) -> list[Rule]:
        return self.rule_repository.find_all_rules_by_user(user)

    def find_last_rule_by_user_id(self, user_id) -> Rule:
        return self.rule_repository.find_last_rule_by_user_id(user_id)
