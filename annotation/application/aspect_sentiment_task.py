from annotation.application.document import AnnotationTask, Label


class AspectSntimentTask(AnnotationTask):

    def __init__(self, document, annotations=()):
        super().__init__(document, annotations)

    def get_dataset_for_analysis(self):
        dataset = {}
        for target_id, target in self.get_targets():
            a_s = []
            if target_id in self.annotations:
                a_s = [self._dump_annotation(a) for a in self.annotations[target_id]]
            
            sentiment = ""
            if len(a_s) > 0:
                score = 0
                for a in a_s:
                    if a["sentiment"] == "positive":
                        score += 1
                    elif a["sentiment"] == "negative":
                        score -= 1
                if score > 0:
                    sentiment = "positive"
                elif score < 0:
                    sentiment = "negative"
                else:
                    sentiment = "neutral"

            dataset[target_id] = {
                "target": target,
                "sentiment": sentiment,
                "annotations": a_s
            }
        return dataset
    
    def _dump_annotation(self, a):
        ea, s = a.label.split(",")
        e, at = ea.split("#")
        return {
            "label": a.label,
            "label_target": a.label_target,
            "sentiment": s,
            "entity": e,
            "attribute": at,
            "position": a.position,
            "annotator": a.annotator
        }

    def get_targets(self):
        results = [d for d in self.document.body if d["category"] == "業績"]
        targets = []
        index = 0
        for r in results:
            _lines = [ln.strip() for ln in r["lines"] if ln.strip()]
            for ln in _lines:
                sub_lines = ln.split("。")
                for sl in sub_lines:
                    if sl.strip():
                        targets.append((int(index), sl.strip()))
                        index += 1
        return targets

    def get_labels(self):
        entity = ["market", "company", "business", "product", "NULL", "OOD"]
        attribute = ["general", "sales", "profit", "amount", "price", "cost"]
        attribute_name = {"general": "全", "sales": "売", "profit": "利",
                          "amount": "量", "price": "販単", "cost": "原単"}
        sentiment = ["positive", "negative", "neutral"]
        sentiment_name = {"positive": "O", "negative": "X", "neutral": "-"}

        labels = []
        for e in entity:
            for a in attribute:
                for s in sentiment:
                    if e == "market" and a != "general":
                        continue
                    if e == "OOD" and a != "general":
                        continue

                    label_name = attribute_name[a] + ":" + sentiment_name[s]
                    label_id = e + "#" + a + "," + s
                    if s == "positive":
                        style = [{"background-color": "#23d160"}, {"color": "white"}]
                    elif s == "negative":
                        style = [{"background-color": "#363636"}, {"color": "white"}]
                    else:
                        style = [{"background-color": "#fff"}, {"color": "#363636"},
                                 {"border": "1px solid #dbdbdb"}]
                    label = Label(label_id, e, label_name, style)
                    labels.append(label)

        return labels
