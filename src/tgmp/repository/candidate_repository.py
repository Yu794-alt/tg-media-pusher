from entities.candidate_entity import Candidate


class CandidateRepository:

    def __init__(self, db_connection):
        self.db_connection = db_connection

    def create_candidate(self, candidate: Candidate):
        connect = self.db_connection

        result = connect.execute("INSERT INTO candidates (tg_id, user_name, name, phone) VALUES(?, ?, ?, ?)",
                                 (candidate.tg_id, candidate.user_name, candidate.name, candidate.phone))
        connect.commit()
        new_rule_id = result.lastrowid
        return new_rule_id

    def find_candidate_by_id(self, id):
        connect = self.db_connection
        cursor = connect.execute("SELECT * FROM candidates WHERE candidates.tg_id = ? ", (id,))
        row = cursor.fetchone()
        cursor.close()

        if row is None:
            return None

        return Candidate(
            row['user_name'],
            row['tg_id'],
            row['name'],
            row['phone'],
            str(row['created_at'])
        )
