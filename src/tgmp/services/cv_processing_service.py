from api.gemini import generate_content


class CVProcessingService:

    @staticmethod
    def get_ai_result(tags, cv_reference):
        json_result = generate_content(tags, cv_reference)
        return json_result