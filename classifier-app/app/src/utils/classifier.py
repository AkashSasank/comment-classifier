import numpy as np
from typing import List
from transformers import AutoConfig, DistilBertTokenizer, \
    DistilBertForSequenceClassification
from transformers.pipelines.image_classification import softmax

from ..schemas.classifier import Comment, CommentInfo


class CommentClassifier:
    def __init__(self):
        self.__MODEL = "distilbert-base-uncased-finetuned-sst-2-english"
        self.tokenizer = DistilBertTokenizer.from_pretrained(self.__MODEL)
        self.config = AutoConfig.from_pretrained(self.__MODEL)
        self.model = DistilBertForSequenceClassification.from_pretrained(self.__MODEL)
        # self.sentiment_task = pipeline("sentiment-analysis", model=self.__MODEL, tokenizer=self.tokenizer)

    def __classify_comment(self, input_string: str):
        encoded_input = self.tokenizer(input_string, return_tensors='pt')
        output = self.model(**encoded_input)
        # output = self.sentiment_task(input_string)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)
        ranking = np.argsort(scores)
        label = self.config.id2label[ranking[-1]]
        score = scores[ranking[-1]]
        return label, score

    def classify(self, comments: List[Comment]) -> List[CommentInfo]:
        """Classify comments"""
        results = []
        for comment in comments:
            label, score = self.__classify_comment(comment.text)
            results.append(CommentInfo(id=comment.id, score="{:.4f}".format(score), comment=comment.text, classification=label))
        return results


classifier = CommentClassifier()
