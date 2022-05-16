from abc import ABC, abstractmethod


class Processor(ABC):
    """The Processor abstract base class provides an interface with
    the process method to ensure concrete classes are properly
    implemented.

    Attributes:

    """

    @abstractmethod
    def process(self):
        """Abstract method expected to be defined in concrete classes."""
        pass
