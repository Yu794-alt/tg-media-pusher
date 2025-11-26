from entities.analytic_record_entiry import AnalyticRecord
from entities.candidate_entity import Candidate
from entities.rule_entity import Rule
from entities.user_entity import User


class AnalyticRecordRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def create_analytic_record(self, analytic_record: AnalyticRecord):
        connect = self.db_connection

        result = connect.execute(
            "INSERT INTO analytic_records (user_id, rule_id, cv_path, ai_result, opinion, is_viewed, candidate_id) VALUES(?, ?, ?, ?, ?, ?,?)",
            (analytic_record.user_id, analytic_record.rule.id, analytic_record.cv_path, analytic_record.ai_result,
             analytic_record.opinion,
             analytic_record.is_viewed, analytic_record.candidate.tg_id))
        connect.commit()
        new_record_id = result.lastrowid
        return new_record_id

    def get_analytic_record_by_user_id(self, user_id) -> list[AnalyticRecord]:
        connect = self.db_connection
        cursor = connect.execute(
            """SELECT ar.id,
                      ar.user_id,
                      ar.rule_id,
                      ar.cv_path,
                      ar.ai_result,
                      ar.opinion,
                      ar.is_viewed,
                      r.id        as rule_id,
                      r.tags      as rule_tags,
                      c.tg_id     as candidate_id,
                      c.user_name as candidate_user_name,
                      c.name      as candidate_name,
                      c.phone     as candidate_phone
               FROM analytic_records ar
                        LEFT JOIN rules r ON ar.rule_id = r.id
                        LEFT JOIN candidates c ON ar.candidate_id = c.tg_id
               WHERE ar.user_id = ? """, (user_id,)
        )
        rows = cursor.fetchall()
        cursor.close()

        analytic_records: list[AnalyticRecord] = []

        if len(rows) == 0:
            return analytic_records

        for row in rows:
            analytic_records.append(AnalyticRecord(
                user_id=row['user_id'],
                rule=Rule(
                    id=row['rule_id'],
                    user=User(),
                    tags=row['rule_tags']
                ),
                cv_path=row['cv_path'],
                ai_result=row['ai_result'],
                opinion=row['opinion'],
                candidate=Candidate(
                    user_name=row['candidate_user_name'],
                    tg_id=row['candidate_id'],
                    name=row['candidate_name'],
                    phone=row['candidate_phone']
                ),
                is_viewed=row['is_viewed']
            ))

        return analytic_records
