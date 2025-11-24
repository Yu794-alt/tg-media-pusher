from factories.repository_factory import RepositoryFactory
from services.analytic_record_service import AnalyticRecordService
from services.candidate_service import CandidateService
from services.rule_service import RuleService
from services.user_service import UserService


class ServiceFactory:
    def __init__(self, repository_factory: RepositoryFactory):
        self.repository_factory = repository_factory

    def create_rule_service(self) -> RuleService:
        return RuleService(self.repository_factory.create_rule_repository())

    def create_analytic_record_service(self) -> AnalyticRecordService:
        return AnalyticRecordService(self.repository_factory.create_analytic_record_repository())

    def create_user_service(self) -> UserService:
        return UserService(self.repository_factory.create_user_repository())

    def create_candidate_service(self) -> CandidateService:
        return CandidateService(self.repository_factory.create_candidate_repository())
