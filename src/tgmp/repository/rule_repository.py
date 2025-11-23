from entities.rule_entity import Rule


class RuleRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def create_rule(self,rule: Rule):
        connect = self.db_connection

        result = connect.execute("INSERT INTO rules (tags, user_id) VALUES(?, ?)",
                                 (rule.tags, rule.user.id))
        connect.commit()
        new_rule_id = result.lastrowid
        return new_rule_id
