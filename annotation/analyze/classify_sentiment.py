import os
import sys
import numpy as np
from sklearn.linear_model import SGDClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
from annotation.application.document import Document
from annotation.application.aspect_sentiment_task import AspectSntimentTask
from annotation.analyze.preprocessor import Preprocessor


DATA_DIR = os.path.join(os.path.dirname(__file__), "../../data/interim")
ANNOTATE_DIR = os.path.join(os.path.dirname(__file__), "../../data/annotated")


def main():
    corpus = []
    labels = []
    label_index = {"positive": 0, "negative": 1, "neutral": 2}
    prep = Preprocessor()
    
    for d_f in os.listdir(DATA_DIR):
        if not d_f.endswith(".jsonl"):
            continue
        d_p = os.path.join(DATA_DIR, d_f)

        doc = Document.load(d_p)
        task = AspectSntimentTask.load(ANNOTATE_DIR, doc)
        if len(task.annotations) == 0:
            continue
        doc_dataset = task.get_dataset_for_analysis()
        for key in doc_dataset:
            line = doc_dataset[key]["target"]
            sentiment = doc_dataset[key]["sentiment"]
            if sentiment:
                corpus.append(prep.tokenize(line, join=True))
                labels.append(label_index[sentiment])
    
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(corpus)
    y = np.array(labels).reshape((-1, 1))
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
    clf = SGDClassifier()
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    labels = sorted(label_index.items(), key=lambda x: x[1])
    labels = [lb[0] for lb in labels]
    print(classification_report(y_test, y_pred, target_names=labels))


if __name__ == "__main__":
    main()
