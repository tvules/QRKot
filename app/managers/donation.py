from app.managers.base import ManagerBase
from app.models.donation import Donation


class DonationManager(ManagerBase):
    model: Donation = Donation


donation_manager = DonationManager()
