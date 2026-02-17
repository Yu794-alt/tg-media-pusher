from entities.analytic_record_entiry import AnalyticRecord
from entities.rule_entity import Rule
from entities.user_entity import User


class RuleRepository:

    def __init__(self, connect):
        self.connect = connect

    def create_rule(self, rule: Rule):
        connect = self.connect

        cursor = connect.execute(
            "INSERT INTO rules (tags, user_id) VALUES(?, ?)",
            (rule.tags, rule.user.id)
        )
        connect.commit()
        new_rule_id = cursor.lastrowid
        return new_rule_id

    def find_rule_by_user(self, user: User):
        connect = self.connect

        row = connect.execute("SELECT id, tags FROM rules WHERE user_id = ? ",
                              (user.id,)).fetchone()
        return Rule(
            row['id'],
            row['tags'],
        )

    def find_all_rules_by_user(self, user: User) -> list[Rule]:
        connect = self.connect

        cursor = connect.execute("""SELECT id, tags, date_start, date_end
                                    FROM rules
                                    WHERE user_id = ?
                                    ORDER BY created_at DESC""",
                                 (user.id,))
        rows = cursor.fetchall()
        cursor.close()

        rules: list[Rule] = []

        if len(rows) == 0:
            return rules

        for row in rows:
            rules.append(Rule(
                id=row['id'],
                user=user,
                tags=row['tags'],
                date_start=str(row['date_start']),
                date_end=str(row['date_end'])
            ))

        return rules

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

    def find_last_rule_by_user_id(self, id):
        """Возвращает последний (по id) rule для заданного user_id."""
        connect = self.connect

        cursor = connect.execute(
            "SELECT id, tags FROM rules WHERE user_id = ? ORDER BY id DESC LIMIT 1",
            (id,)
        )
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
