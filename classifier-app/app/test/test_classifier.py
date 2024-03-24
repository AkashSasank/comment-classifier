from fastapi.testclient import TestClient
import pytest
from ..src.application import create_application
from ..src.api.utils import filter_comments, order_comments
from ..src.utils.classifier import classifier

app = create_application()

client = TestClient(app)


class TestClassifierAPI:
    start_time = None
    end_time = None
    order_by = None

    @pytest.mark.usefixtures
    def test_comments_classifier_success(self, mock_feddit_get,
                                         feddit_comments_objects,
                                         feddit_comments_json,
                                         feddit_comments_classification_objects):
        assert mock_feddit_get.return_value.json() == feddit_comments_json
        filtered_comments = filter_comments(feddit_comments_objects,
                                            start_time=self.start_time,
                                            end_time=self.end_time)
        comments = classifier.classify(filtered_comments)
        comments = order_comments(comments, order_by=None)
        assert comments == feddit_comments_classification_objects
