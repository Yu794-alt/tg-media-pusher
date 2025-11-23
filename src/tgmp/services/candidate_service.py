from entities.candidate_entity import Candidate
from repository.candidate_repository import CandidateRepository

class CandidateService:
    def __init__(self, candidate_repository : CandidateRepository):
        self.candidate_repository = candidate_repository


    def create_user(self,candidate: Candidate):
        return self.candidate_repository.create_candidate(candidate)
