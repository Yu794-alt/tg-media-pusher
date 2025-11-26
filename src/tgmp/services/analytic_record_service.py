from entities.analytic_record_entiry import AnalyticRecord
from entities.candidate_entity import Candidate
from entities.rule_entity import Rule
from entities.user_entity import User
from repository.analytic_record_repository import AnalyticRecordRepository


class AnalyticRecordService:

    def __init__(self, analytic_record_repository: AnalyticRecordRepository):
        self.analytic_record_repository = analytic_record_repository

    def create_analytic_record(self, analytic_record: AnalyticRecord):
        return self.analytic_record_repository.create_analytic_record(analytic_record)

    def get_analytic_record_by_user_id(self, user_id) -> list[AnalyticRecord]:
        return self.analytic_record_repository.get_analytic_record_by_user_id(user_id)
