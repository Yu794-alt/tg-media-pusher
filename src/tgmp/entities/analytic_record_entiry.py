from entities.candidate_entity import Candidate
from entities.rule_entity import Rule


class AnalyticRecord:
    def __init__(self, user_id, rule: Rule, cv_path: str, ai_result: str, opinion: str, candidate,
                 is_viewed: bool = False,
                 ):
        self.user_id = user_id
        self.rule: Rule = rule
        self.cv_path: str = cv_path
        self.ai_result: str = ai_result
        self.opinion: str = opinion
        self.is_viewed: bool = is_viewed
        self.candidate: Candidate = candidate
