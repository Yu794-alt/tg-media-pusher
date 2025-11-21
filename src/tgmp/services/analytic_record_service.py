from entities.analytic_record_entiry import AnalyticRecord
from entities.candidate_entity import Candidate
from entities.rule_entity import Rule
from entities.user_entity import User
from repository.analytic_record_repository import AnalyticRecordRepository


class AnalyticRecordService:

    @staticmethod
    def create_user(analytic_record: AnalyticRecord, user: User, rule: Rule, candidate: Candidate):
        return AnalyticRecordRepository.analytic_record_candidate(analytic_record, user, rule, candidate)
