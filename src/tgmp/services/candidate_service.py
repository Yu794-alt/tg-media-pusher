from ipaddress import collapse_addresses

from entities.candidate_entity import Candidate
from repository.candidate_repository import CandidateRepository


class CandidateService:

    def __init__(self, candidate_repository: CandidateRepository):
        self.candidate_repository = candidate_repository

    def create_candidate(self, candidate: Candidate):
        return self.candidate_repository.create_candidate(candidate)

    def get_or_create_candidate(self, candidate: Candidate) -> Candidate:
        candidate_db = self.candidate_repository.find_candidate_by_id(candidate.tg_id)
        if candidate_db is None:
            self.candidate_repository.create_candidate(candidate)
            return candidate
        return candidate_db
