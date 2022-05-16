from abc import ABCMeta
from classes import Processor


def test_processor():
    Processor.__abstractmethods__ = set()

    p = Processor()
    data = p.process()
    assert isinstance(Processor, ABCMeta)
    assert data is None
