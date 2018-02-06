import os
import shutil
import json


class Document():

    def __init__(self,
                 doc_id, doc_text, edi_id, company_name,
                 body, topic):
        self.doc_id = doc_id
        self.doc_text = doc_text
        self.edi_id = edi_id
        self.company_name = company_name
        self.body = body
        self.topic = topic

    def get_header(self):
        return {
            "document_id": self.document_id,
            "document_name": self.document_name,
            "doc_text": self.doc_text,
            "edi_id": self.edi_id
        }

    @property
    def document_id(self):
        return self.edi_id

    @property
    def document_name(self):
        return self.company_name

    @classmethod
    def load(cls, file_path):
        if not os.path.isfile(file_path):
            raise Exception("File {} does not found.".format(file_path))

        with open(file_path, encoding="utf-8") as f:
            doc = json.load(f)

        doc_id = doc["doc_id"]
        doc_text = doc["doc_text"]
        edi_id = doc["edi_id"]
        company_name = doc["company_name"]
        body = doc["body"]
        topic = doc["topic"]
        return cls(doc_id, doc_text, edi_id, company_name, body, topic)


class Label():

    def __init__(self, label, label_group="", display_name="", display_style=""):
        self.label = label
        self.label_group = label_group
        self.display_name = display_name
        self.display_style = display_style
    
    def dumps(self):
        return {
            "label": self.label,
            "label_group": self.label_group,
            "display_name": self.display_name,
            "display_style": self.display_style
        }


class Annotation():

    def __init__(self, target_id, target, label, label_target="", position=(), annotator="anonymous"):
        self.target_id = int(target_id)
        self.target = target
        self.label = label
        self.label_target = label_target
        self.position = position
        if len(self.position) > 0:
            self.position = [int(i) for i in self.position]
        self.annotator = annotator

    def dumps(self):
        a = {
            "target_id": self.target_id,
            "target": self.target,
            "label": self.label,
            "label_target": self.label_target,
            "position": self.position,
            "annotator": self.annotator
        }
        return a
    
    @classmethod
    def loads(cls, obj):
        a = Annotation(
            obj["target_id"],
            obj["target"],
            obj["label"],
            obj["label_target"],
            obj["position"] if "position" in obj else ()
        )
        if "annotator" in obj:
            a.annotator = obj["annotator"]
        return a


class AnnotationTask():
    ANNOTATION_CLASS = Annotation

    def __init__(self, document, annotations=()):
        self.document = document
        self.annotations = {} if len(annotations) == 0 else annotations

    def get_targets(self):
        raise Exception("Sub class have to specify texts for annotation")

    def get_labels(self):
        raise Exception("Sub class have to define label candidates")

    def get_dataset(self):
        dataset = {}
        for target_id, target in self.get_targets():
            a_s = []
            if target_id in self.annotations:
                a_s = [a.dumps() for a in self.annotations[target_id]]
            
            dataset[target_id] = {
                "target": target,
                "annotations": a_s
            }
        return dataset

    def save_annotations(self, target_dir, annotation_objs, annotator):
        _dir = os.path.join(target_dir, self.document.document_id)
        annotations = [self.ANNOTATION_CLASS.loads(a_obj) 
                       for a_obj in annotation_objs]
        if annotator:
            for a in annotations:
                a.annotator = annotator
            if os.path.exists(_dir):
                for f in os.listdir(_dir):
                    if f.startswith("ann__") and f.endswith("__{}.json".format(annotator)):
                        os.remove(os.path.join(_dir, f))

        save_bucket = {}
        for a in annotations:
            key = (a.target_id, a.annotator)
            if key not in save_bucket:
                save_bucket[key] = []
            save_bucket[key].append(a)

        if len(save_bucket) > 0 and not os.path.exists(_dir):
            os.mkdir(_dir)

        for key in save_bucket:
            file_name = self._make_annotation_file_name(*key)
            body = {
                "annotations": [a.dumps() for a in save_bucket[key]]
            }
            file_path = os.path.join(_dir, file_name)
            with open(file_path, mode="w", encoding="utf-8") as f:
                json.dump(body, f, ensure_ascii=False, indent=2)

    def _make_annotation_file_name(self, target_id, annotator):
        return "ann__{}__{}__{}.json".format(self.document.document_id, target_id, annotator)

    @classmethod
    def load(cls, target_dir, document, annotator=""):
        annotations = {}
        _dir = os.path.join(target_dir, document.document_id)
        if os.path.exists(_dir):
            for f in sorted(os.listdir(_dir)):
                if not f.startswith("ann__"):
                    continue
                if annotator and not f.endswith("__{}.json".format(annotator)):
                    continue
                path = os.path.join(_dir, f)
                with open(path, encoding="utf-8") as af:
                    annotation_objs = json.load(af)["annotations"]
                    a_list = [cls.ANNOTATION_CLASS.loads(a_obj) for a_obj in annotation_objs]
                    if len(a_list) > 0:
                        target_id = a_list[0].target_id
                        if target_id not in annotations:
                            annotations[target_id] = a_list
                        else:
                            annotations[target_id] += a_list

        instance = cls(document, annotations)
        return instance
