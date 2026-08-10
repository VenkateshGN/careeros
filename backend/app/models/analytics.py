class UserAnalyticsModelMock:
    def __init__(self, user_id, total_applications, interviews_scheduled, offers_received, rejection_rate, skill_growth, updated_at):
        self.user_id = user_id
        self.total_applications = total_applications
        self.interviews_scheduled = interviews_scheduled
        self.offers_received = offers_received
        self.rejection_rate = rejection_rate
        self.skill_growth = skill_growth
        self.updated_at = updated_at

# SQLAlchemy implementations would go here
