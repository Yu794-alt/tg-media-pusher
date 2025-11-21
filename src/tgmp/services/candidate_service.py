from entities.candidate_entity import Candidate
from repository.candidate_repository import CandidateRepository

class CandidateService:

    @staticmethod
    def create_user(candidate: Candidate):
        return CandidateRepository.create_candidate(candidate)
