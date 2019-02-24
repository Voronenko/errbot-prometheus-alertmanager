from datetime import datetime, timedelta
import pytz
from unittest import TestCase
from amtoolhelper import AmtoolHelper

ALERTMANAGER_HOST = "http://10.9.0.138:9093/api/v2"


class TestAmtoolHelper(TestCase):
    def test_get_status(self):
        amtoolhelper = AmtoolHelper(alertmanager_address=ALERTMANAGER_HOST)
        amtoolhelper.get_status()

    def test_get_alerts(self):
        amtoolhelper = AmtoolHelper(alertmanager_address=ALERTMANAGER_HOST)
        alerts = amtoolhelper.get_alerts()
        self.assertIsNotNone(alerts)

    def test_get_alerts_with_filter(self):
        amtoolhelper = AmtoolHelper(alertmanager_address=ALERTMANAGER_HOST)
        filter = amtoolhelper.get_filters_by_terms(["env=live"])
        alerts = amtoolhelper.get_alerts(filter=filter)
        self.assertIsNotNone(alerts)

    def test_get_alert(self):
        amtoolhelper = AmtoolHelper(alertmanager_address=ALERTMANAGER_HOST)
        alert = amtoolhelper.get_alert('af2442fa7f7ee655')
        self.assertIsNotNone(alert)

    def test_get_silences(self):
        amtoolhelper = AmtoolHelper(alertmanager_address=ALERTMANAGER_HOST)
        silences = amtoolhelper.get_silences()
        self.assertIsNotNone(silences)

    def test_get_silence(self):
        amtoolhelper = AmtoolHelper(alertmanager_address=ALERTMANAGER_HOST)
        silence = amtoolhelper.get_silence(silence_id="bb788860-35d2-48e7-9062-f082c77d202d")
        self.assertIsNotNone(silence)

    def test_post_silence_suppress(self):
        amtoolhelper = AmtoolHelper(alertmanager_address=ALERTMANAGER_HOST)
        start_period = datetime.now(pytz.timezone('Europe/Kiev'))
        end_period = start_period + timedelta(minutes=1)

        alert = amtoolhelper.get_alert('af2442fa7f7ee655')
        matchers = amtoolhelper.get_matchers_by_alert(alert)

        silence = amtoolhelper.post_silence(
            matchers=matchers,
            starts_at=start_period.isoformat(),
            ends_at=end_period.isoformat(),
            created_by="Someone",
            comment="test silence"
        )
        self.assertIsNotNone(silence)

    def test_post_silence_selective(self):
        amtoolhelper = AmtoolHelper(alertmanager_address=ALERTMANAGER_HOST)
        start_period = datetime.now(pytz.timezone('Europe/Kiev'))
        end_period = start_period + timedelta(minutes=1)

        alert = amtoolhelper.get_alert('af2442fa7f7ee655')
        matchers = amtoolhelper.get_matchers_by_terms(terms=["~StrategyDown2", "instance=i-049a6b9bbbb6fb76b"])

        silence = amtoolhelper.post_silence(
            matchers=matchers,
            starts_at=start_period.isoformat(),
            ends_at=end_period.isoformat(),
            created_by="Someone",
            comment="test silence"
        )
        self.assertIsNotNone(silence)
