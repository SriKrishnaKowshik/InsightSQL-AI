import ollama


class FollowUpGenerator:

    def generate(self, question: str, sql: str):

        prompt = f"""
You are a Business Intelligence assistant.

A user asked:

{question}

Generated SQL:

{sql}

Suggest exactly 3 short follow-up business questions.

Rules:
- Maximum 12 words each
- Relevant to the previous analysis
- Do not number them
- One question per line
- Do not explain anything
"""

        response = ollama.chat(
            model="gemma3:4b",
            messages=[{"role": "user", "content": prompt}]
        )

        text = response["message"]["content"]

        suggestions = [
            line.strip("-•123456789. ").strip()
            for line in text.split("\n")
            if line.strip()
        ]

        return suggestions[:3]