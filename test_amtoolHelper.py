from datetime import datetime, timedelta
import pytz
from unittest import TestCase
from amtoolhelper import AmtoolHelper
import parsedatetime as pdt  # $ pip install parsedatetime

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
        silences = amtoolhelper.get_silences(filter=[])
        self.assertIsNotNone(silences)

    def test_expired_silences(self):
        amtoolhelper = AmtoolHelper(alertmanager_address=ALERTMANAGER_HOST)
        silences = amtoolhelper.get_silences(filter=[], expired=True)
        self.assertIsNotNone(silences)

    def test_nonexpired_within_silences(self):
        amtoolhelper = AmtoolHelper(alertmanager_address=ALERTMANAGER_HOST)
        silences = amtoolhelper.get_silences(filter=[], expired=False, within="1h")
        self.assertIsNotNone(silences)

    def test_expired_within_silences(self):
        amtoolhelper = AmtoolHelper(alertmanager_address=ALERTMANAGER_HOST)
        silences = amtoolhelper.get_silences(filter=[], expired=True, within="1h")
        self.assertIsNotNone(silences)

    def test_get_silence(self):
        amtoolhelper = AmtoolHelper(alertmanager_address=ALERTMANAGER_HOST)
        silence = amtoolhelper.get_silence(silence_id="bb788860-35d2-48e7-9062-f082c77d202d")
        self.assertIsNotNone(silence)

    def test_post_silence_suppress(self):
        amtoolhelper = AmtoolHelper(alertmanager_address=ALERTMANAGER_HOST)
        start_period = datetime.now(pytz.timezone('Europe/Kiev'))
        end_period = start_period + timedelta(minutes=1)

        alert = amtoolhelper.get_alert('ee5d73c3f0a498f1')
        matchers = amtoolhelper.get_matchers_by_alert(alert, ["name", "role"])

        silence = amtoolhelper.post_silence(
            matchers=matchers,
            starts_at=start_period.isoformat(),
            ends_at=end_period.isoformat(),
            created_by="Someone",
            comment="test silence"
        )
        self.assertIsNotNone(silence)

    def test_post_silence_add(self):
        amtoolhelper = AmtoolHelper(alertmanager_address=ALERTMANAGER_HOST)
        start_period = datetime.now().utcnow()

        cal = pdt.Calendar()
        diff = cal.parseDT("1h", sourceTime=datetime.min)[
                       0] - datetime.min
        end_period = start_period + diff

        utc = pytz.UTC
        start_period = utc.localize(start_period)
        end_period = utc.localize(end_period)

        parsed_matchers = amtoolhelper.get_matchers_by_terms(["instance=i-049a6b9bbbb6fb76b"])
        silence = amtoolhelper.post_silence(
            matchers=parsed_matchers,
            starts_at=start_period.isoformat(),
            ends_at=end_period.isoformat(),
            created_by="errbot",
            comment="test comment"
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

    def test_post_silence_selective(self):
        amtoolhelper = AmtoolHelper(alertmanager_address=ALERTMANAGER_HOST)
        parsed_matchers = amtoolhelper.get_matchers_by_terms(["instance=222"])
        tuples = amtoolhelper.convert_matchers_to_tuples(parsed_matchers)
