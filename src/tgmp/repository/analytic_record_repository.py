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
            (analytic_record.user_id, analytic_record.rule_id, analytic_record.cv_path, analytic_record.ai_result,
             analytic_record.opinion,
             analytic_record.is_viewed, analytic_record.candidate_id))
        connect.commit()
        new_record_id = result.lastrowid
        return new_record_id
