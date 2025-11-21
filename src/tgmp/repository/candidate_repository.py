from entities.candidate_entity import Candidate
from src.tgmp import app


class CandidateRepository:

    @staticmethod
    def create_candidate(candidate: Candidate):
        connect = app.config["db_connect"]

        result = connect.execute("INSERT INTO candidates (tg_id, user_name, name, phone) VALUES(?, ?, ?, ?)",
                                 (candidate.tg_id, candidate.user_name, candidate.name, candidate.phone))
        connect.commit()
        new_rule_id = result.lastrowid
        return new_rule_id
