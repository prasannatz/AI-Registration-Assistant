import json

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


class IntentClassifier:

    def __init__(self, intents_file="intents.json"):

        self.intents_file = intents_file

        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2)
        )

        self.model = LogisticRegression(
            max_iter=1000
        )

        self.train()

    def train(self):

        # Load training data
        with open(
            self.intents_file,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        training_sentences = []
        training_labels = []

        # Prepare training examples
        for intent in data["intents"]:

            tag = intent["tag"]

            for pattern in intent["patterns"]:

                training_sentences.append(pattern)
                training_labels.append(tag)

        # Convert text into TF-IDF features
        X = self.vectorizer.fit_transform(
            training_sentences
        )

        # Train Logistic Regression model
        self.model.fit(
            X,
            training_labels
        )

    def predict(self, text):

        X = self.vectorizer.transform([text])

        prediction = self.model.predict(X)

        return prediction[0]


if __name__ == "__main__":

    classifier = IntentClassifier()

    print("AI Intent Classifier")
    print("--------------------")

    test_messages = [
        "hello",
        "I want to register",
        "can you help me",
        "thank you",
        "goodbye"
    ]

    for message in test_messages:

        intent = classifier.predict(message)

        print(
            f"Message: {message}"
        )

        print(
            f"Predicted intent: {intent}\n"
        )