from app.exceptions.base import BaseDetailException, DoesNotExist


class DonationException(BaseDetailException):
    """Base Donation exception."""

    pass


class DonationDoesNotExist(DoesNotExist, DonationException):
    pass
