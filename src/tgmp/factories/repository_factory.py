from repository.analytic_record_repository import AnalyticRecordRepository
from repository.candidate_repository import CandidateRepository
from repository.rule_repository import RuleRepository
from repository.user_repository import UserRepository
from services.infrastructure.db_service import DbService


class RepositoryFactory:
    def __init__(self, db_connection):
        self.db_connection = DbService.get_db_connection(db_connection)

    def create_user_repository(self) -> UserRepository:
        return UserRepository(self.db_connection)

    def create_analytic_record_repository(self) -> AnalyticRecordRepository:
        return AnalyticRecordRepository(self.db_connection)

    def create_rule_repository(self) -> RuleRepository:
        return RuleRepository(self.db_connection)

    def create_candidate_repository(self) -> CandidateRepository:
        return CandidateRepository(self.db_connection)
