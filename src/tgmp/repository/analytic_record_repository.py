from entities.analytic_record_entiry import AnalyticRecord
from entities.candidate_entity import Candidate
from entities.rule_entity import Rule
from entities.user_entity import User
from src.tgmp import app


class AnalyticRecordRepository:

    @staticmethod
    def analytic_record_candidate(analytic_record: AnalyticRecord, user: User, rule: Rule, candidate: Candidate):
        connect = app.config["db_connect"]

        result = connect.execute(
            "INSERT INTO analytic_records (user_id, rule_id, cv_path, ai_result, opinion, is_viewed, candidate_id) VALUES(?, ?, ?, ?, ?, ?,?)",
            (user.id, rule.id, analytic_record.cv_path, analytic_record.ai_result, analytic_record.opinion,
             analytic_record.is_viewed, candidate.tg_id))
        connect.commit()
        new_rule_id = result.lastrowid
        return new_rule_id
