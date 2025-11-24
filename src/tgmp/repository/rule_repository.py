from entities.rule_entity import Rule
from entities.user_entity import User


class RuleRepository:

    def __init__(self, connect):
        self.connect = connect

    def create_rule(self, rule: Rule):
        connect = self.connect

        result = connect.execute("INSERT INTO rules (tags, user_id) VALUES(?, ?)",
                                 (rule.tags, rule.user.id)).fetchone()
        connect.commit()
        new_rule_id = result.lastrowid
        return new_rule_id

    def find_rule_by_user(self, user: User):
        connect = self.connect

        row = connect.execute("SELECT id, tags FROM rules WHERE user_id = ? ",
                              (user.id,)).fetchone()
        return Rule(
            row['id'],
            row['tags'],
        )

    def find_rule_by_user_id(self, id):
        connect = self.connect

        cursor = connect.execute("SELECT id, tags FROM rules WHERE user_id = ? ",
                                 (id,))
        row = cursor.fetchone()
        cursor.close()

        if row is None:
            return None

        return Rule(
            id=row['id'],
            user=User(
                id=96,
                login='qweqweqwe'
            ),
            tags=row['tags'],
        )
