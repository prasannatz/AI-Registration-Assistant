import re
import nltk
from nltk.stem import WordNetLemmatizer


class RegistrationAssistant:

    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.user_data = {}
        self.state = "idle"

    def reset(self):
        self.user_data = {}
        self.state = "idle"

    def preprocess_text(self, text):
        text = text.lower()

        text = re.sub(
            r"[^a-zA-Z0-9@._+\-\s]",
            " ",
            text
        )

        tokens = nltk.word_tokenize(text)

        tokens = [
            self.lemmatizer.lemmatize(token)
            for token in tokens
            if token.strip()
        ]

        return tokens

    def classify_intent(self, text):

        text_lower = text.lower()
        tokens = self.preprocess_text(text)

        if (
            "hello" in text_lower
            or "hi" in tokens
            or "hey" in tokens
        ):
            return "greeting"

        if (
            "register" in text_lower
            or "registration" in text_lower
            or "apply" in text_lower
            or "sign up" in text_lower
            or "want to register" in text_lower
        ):
            return "register"

        if (
            "help" in text_lower
            or "support" in text_lower
            or "guide" in text_lower
        ):
            return "help"

        if (
            "thank" in text_lower
            or "thanks" in text_lower
        ):
            return "thank_you"

        if (
            "bye" in text_lower
            or "goodbye" in text_lower
        ):
            return "bye"

        return "unknown"

    def extract_name(self, text):

        match = re.search(
            r"\b(?:my name is|i am|i'm)\s+([A-Za-z][A-Za-z .'-]{1,50})",
            text,
            re.IGNORECASE
        )

        if match:

            name = match.group(1).strip()

            name = re.split(
                r"\b(?:and|my email|email is|i study)\b",
                name,
                flags=re.IGNORECASE
            )[0].strip()

            return name

        return None

    def extract_email(self, text):

        match = re.search(
            r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[A-Za-z]{2,}\b",
            text
        )

        if match:
            return match.group(0)

        return None

    def validate_email(self, email):

        pattern = (
            r"^[a-zA-Z0-9._%+-]+"
            r"@[a-zA-Z0-9.-]+\."
            r"[A-Za-z]{2,}$"
        )

        return bool(re.fullmatch(pattern, email))

    def get_missing_field(self):

        required_fields = [
            "name",
            "email",
            "field",
            "experience"
        ]

        for field in required_fields:

            if field not in self.user_data:
                return field

        return None

    def confirmation(self):

        return (
            "Registration confirmed! 🎉\n\n"
            f"Name: {self.user_data['name']}\n"
            f"Email: {self.user_data['email']}\n"
            f"Field of study: {self.user_data['field']}\n"
            f"Programming experience: {self.user_data['experience']}\n\n"
            "Your registration has been completed successfully."
        )

    def handle_message(self, message):

        message = message.strip()

        if not message:
            return "Please enter a message."

        # -------------------------------------------------
        # IMPORTANT:
        # First process registration information.
        # This prevents names/emails from being mistaken
        # for a new "register" command.
        # -------------------------------------------------

        name = self.extract_name(message)

        if name:
            self.user_data["name"] = name

            if self.state == "idle":
                self.state = "collecting"

            return (
                f"Nice to meet you, {name}! 😊\n"
                "Please provide your email address."
            )

        email = self.extract_email(message)

        if email:

            if not self.validate_email(email):
                return (
                    "That email address is not valid. "
                    "Please enter a valid email."
                )

            self.user_data["email"] = email

            if self.state == "idle":
                self.state = "collecting"

            return (
                f"Thank you! Your email {email} has been recorded. 📧\n"
                "Now, please tell me your field of study."
            )

        # -------------------------------------------------
        # YES / CONFIRM
        # -------------------------------------------------

        if (
            message.lower() in
            ["yes", "confirm", "confirmed"]
        ):

            if self.state == "collecting":

                missing = self.get_missing_field()

                if missing:
                    return (
                        f"Please provide your {missing} first."
                    )

                return self.confirmation()

        # -------------------------------------------------
        # REGISTRATION FLOW
        # -------------------------------------------------

        if self.state == "collecting":

            missing = self.get_missing_field()

            if missing == "name":

                return (
                    "Please provide your full name.\n"
                    "Example: My name is Rahul Kumar"
                )

            if missing == "email":

                return (
                    f"Nice to meet you, "
                    f"{self.user_data['name']}! 😊\n"
                    "Please provide your email address."
                )

            if missing == "field":

                self.user_data["field"] = message

                return (
                    "Thank you! 👍\n"
                    "Now tell me about your programming experience.\n"
                    "For example: Beginner, Intermediate, or Advanced."
                )

            if missing == "experience":

                self.user_data["experience"] = message

                return (
                    "Perfect! I have collected all your information.\n\n"
                    "Would you like me to confirm your registration?\n"
                    "Type 'yes' to confirm."
                )

        # -------------------------------------------------
        # NORMAL INTENT CLASSIFICATION
        # -------------------------------------------------

        intent = self.classify_intent(message)

        if intent == "greeting":

            return (
                "Hello! 👋 Welcome to the AI Registration Assistant.\n\n"
                "I can help you complete your internship registration.\n"
                "Type 'register' to begin."
            )

        if intent == "help":

            return (
                "I can help you with:\n"
                "• Internship registration\n"
                "• Collecting your information\n"
                "• Validating your email\n"
                "• Registration confirmation"
            )

        if intent == "thank_you":

            return (
                "You're welcome! 😊 "
                "Is there anything else I can help you with?"
            )

        if intent == "bye":

            return (
                "Thank you for using the AI Registration Assistant. "
                "Goodbye! 👋"
            )

        if intent == "register":

            self.state = "collecting"
            self.user_data = {}

            return (
                "Great! I'll help you register for the internship. 🎓\n\n"
                "Please provide your full name."
            )

        return (
            "I'm not sure I understood that.\n"
            "You can say 'register', 'help', or 'hello'."
        )