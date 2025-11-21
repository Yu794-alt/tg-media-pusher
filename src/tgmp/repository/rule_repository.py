from entities.rule_entity import Rule
from src.tgmp import app


class RuleRepository:

    @staticmethod
    def create_rule(rule: Rule):
        connect = app.config["db_connect"]

        result = connect.execute("INSERT INTO rules (tags, user_id) VALUES(?, ?)",
                                 (rule.tags, rule.user.id))
        connect.commit()
        new_rule_id = result.lastrowid
        return new_rule_id
