from entities.candidate_entity import Candidate


class AnalyticRecord:
    def __init__(self, tags: str, cv_path: str, ai_result: str, opinion: str, candidate: Candidate):
        self.user_id = None | str
        self.tags: str = tags
        self.cv_path: str = cv_path
        self.ai_result: str = ai_result
        self.opinion: str = opinion
        self.is_viewed: bool = False
        self.candidate: Candidate = candidate
