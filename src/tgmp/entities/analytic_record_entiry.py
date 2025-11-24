from entities.candidate_entity import Candidate


class AnalyticRecord:
    def __init__(self, user_id, rule_id: int, cv_path: str, ai_result: str, opinion: str, candidate_id):
        self.user_id = user_id
        self.rule_id: int = rule_id
        self.cv_path: str = cv_path
        self.ai_result: str = ai_result
        self.opinion: str = opinion
        self.is_viewed: bool = False
        self.candidate_id = candidate_id
