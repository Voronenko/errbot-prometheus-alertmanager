from datetime import datetime, timedelta
import dateparser
import pytz
from errbot import arg_botcmd, botcmd, BotPlugin
from amtoolhelper import AmtoolHelper
import parsedatetime as pdt  # $ pip install parsedatetime


def get_ts():
    now = datetime.now()
    return '%s.%d' % (now.strftime('%Y%m%d-%H%M%S'), now.microsecond)


class SaAmtool(BotPlugin):

    def get_configuration_template(self):
        return {
            'server_address': 'https://host:9093/api/v2',
            'time_zone': 'Europe/Kiev'
        }

    @botcmd(template='amtool_status')
    def amtool_status(self, mess, args):
        """Returns alert manager status"""
        self.log.info("Current config {0}".format(self.config))
        self.log.info(
            "Alertmanager @ {0}".format(self.config['server_address']))
        helper = AmtoolHelper(
            alertmanager_address=self.config['server_address'])
        result = helper.get_status()
        return result

    @botcmd(template='amtool_alerts')
    def amtool_alerts(self, mess, args):
        """Returns current alerts list"""
        helper = AmtoolHelper(
            alertmanager_address=self.config['server_address'])
        result = helper.get_alerts()
        return result

    @arg_botcmd('fingerprint', type=str)
    def amtool_alert_describe(self, mess, fingerprint):
        """Returns specific silence details"""
        helper = AmtoolHelper(
            alertmanager_address=self.config['server_address'])
        result = helper.get_alert(fingerprint)
        self.send_card(title=result["annotations"]["title"],
                       body=result["annotations"]["description"],
                       #                       thumbnail='https://raw.githubusercontent.com/errbotio/errbot/master/docs/_static/errbot.png',
                       #                       image='https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png',
                       link=result["generatorURL"],
                       fields=result["labels"].items(),
                       color='blue',
                       in_reply_to=mess)

    @botcmd(template='amtool_silences')
    def amtool_silences(self, mess, args):
        """Returns current silences list"""
        helper = AmtoolHelper(
            alertmanager_address=self.config['server_address'])
        result = helper.get_silences()
        return {"silences": result}

    @arg_botcmd('silence_id', type=str, template='amtool_silence_details')
    def amtool_silence_describe(self, mess, silence_id):
        """Returns specific silence details"""
        helper = AmtoolHelper(
            alertmanager_address=self.config['server_address'])
        result = helper.get_silence(silence_id)
        return result

    @botcmd(template='amtool_recievers')
    def amtool_receivers(self, mess, args):
        """Returns current receivers list"""
        helper = AmtoolHelper(
            alertmanager_address=self.config['server_address'])
        result = helper.get_receivers()
        return result

    @botcmd(template='amtool_alerts_brief')
    def amtool_brief(self, mess, args):
        """Returns brief on alerts"""
        helper = AmtoolHelper(
            alertmanager_address=self.config['server_address'])
        result = helper.get_alerts()
        return result

    @arg_botcmd('--weeks', type=int, default=0)
    @arg_botcmd('--days', type=int, default=0)
    @arg_botcmd('--hours', type=int, default=0)
    @arg_botcmd('--minutes', type=int, default=0)
    @arg_botcmd('--author', type=str, default="errbot")
    @arg_botcmd('--comment', type=str, default="")
    @arg_botcmd('criteria', type=str, metavar='criteria', nargs='+', default=[])
    def amtool_suppress(self, mess, author="errbot", comment="", weeks=0, days=0, hours=0, minutes=0, criteria=[]):
        """Puts exact suppress match on alert"""
        helper = AmtoolHelper(
            alertmanager_address=self.config['server_address'])

        start_period = datetime.now(pytz.timezone(self.config['time_zone']))
        if weeks+days+hours+minutes == 0:
            hours = 1
        end_period = start_period + timedelta(minutes=minutes, hours=hours,
                                              days=days, weeks=weeks)
        self.log.info("Suppressing {0}->{1}".format(start_period, end_period))
        fingerprint = criteria.pop(0)
        self.log.info("Getting alert by fingerprint {0}".format(fingerprint))
        alert = helper.get_alert(fingerprint)
        matchers = helper.get_matchers_by_alert(alert, include_terms=criteria)
        self.log.info("Matchers {0}".format(matchers))
        result = helper.post_silence(
            matchers=matchers,
            starts_at=start_period.isoformat(),
            ends_at=end_period.isoformat(),
            created_by=author,
            comment=comment
        )
        self.send_card(title="Alert suppressed until {0}".format(end_period),
                    body="Alert created by {0} with description '{1}'. To cancel  !amtool silence expire {2}".format(author, comment, result.silence_id),
                    #                       thumbnail='https://raw.githubusercontent.com/errbotio/errbot/master/docs/_static/errbot.png',
                    #                       image='https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png',
                    # link=result["generatorURL"],
                    fields=helper.convert_matchers_to_tuples(matchers),
                    color='blue',
                    in_reply_to=mess)


    @arg_botcmd('--inhibited', dest='inhibited', action='store_true')
    @arg_botcmd('--silenced', dest='silenced', action='store_true')
    @arg_botcmd('--active', dest='active', action='store_true')
    @arg_botcmd('--unprocessed', dest='unprocessed', action='store_true')
    @arg_botcmd('--receiver', dest='receiver', type=str, default="")
    @arg_botcmd('matchers', type=str, metavar='matchers', nargs='+',
                template='amtool_alert_query')
    def amtool_alert_query(self, mess, inhibited=False, silenced=False,
        active=False, unprocessed=False, receiver="", matchers=[]):
        """
          Queries alert in amtool command style
          --inhibited          Show inhibited alerts
          --silenced           Show silenced alerts
          --active             Show active alerts
          --unprocessed        Show unprocessed alerts
          --receiver=RECEIVER  Show alerts matching receiver (Supports regex syntax)

        Args:
          [<matcher-groups>]  Query filter
        """
        if not (inhibited or silenced or active or unprocessed):
            inhibited = True
            silenced = True
            active = True
            unprocessed = True
        self.log.info("matchers {0}".format(matchers))
        helper = AmtoolHelper(
            alertmanager_address=self.config['server_address'])
        filter = helper.get_filters_by_terms(matchers)
        result = helper.get_alerts(
            active=active,
            silenced=silenced,
            inhibited=inhibited,
            unprocessed=unprocessed,
            filter=filter,
            receiver=receiver
        )
        return result

    @arg_botcmd('--author', type=str, default="errbot")
    @arg_botcmd('--duration', type=str, default="1 minute")
    @arg_botcmd('--start', type=str, default=None)
    @arg_botcmd('--end', type=str, default=None)
    @arg_botcmd('--comment', type=str, default="")
    @arg_botcmd('matchers', type=str, metavar='matchers', nargs='+',
                template='amtool_silence_add')
    def amtool_silence_add(self, mess, author, duration, start, end, comment,
        matchers):
        """
            usage: !amtool silence add [<flags>] [<matcher-groups>...]

            Add a new alertmanager silence

                Amtool uses a simplified Prometheus syntax to represent silences. The
                non-option section of arguments constructs a list of "Matcher Groups"
                that will be used to create a number of silences. The following examples
                will attempt to show this behaviour in action:

                !amtool silence add alertname=foo node=bar

                    This statement will add a silence that matches alerts with the
                    alertname=foo and node=bar label value pairs set.

                !amtool silence add foo node=bar

                    If alertname is omitted and the first argument does not contain a '=' or a
                    '=~' then it will be assumed to be the value of the alertname pair.

                !amtool silence add 'alertname=~foo.*'

                    As well as direct equality, regex matching is also supported. The '=~' syntax
                    (similar to Prometheus) is used to represent a regex match. Regex matching
                    can be used in combination with a direct match.

              --author="slavko"  Username for CreatedBy field
              --duration="1h"    Duration of silence
              --start=START      Set when the silence should start. RFC3339 format 2006-01-02T15:04:05-07:00
              --end=END          Set when the silence should end (overwrites duration). RFC3339 format 2006-01-02T15:04:05-07:00
              --comment=COMMENT  A comment to help describe the silence

        """
        helper = AmtoolHelper(
            alertmanager_address=self.config['server_address'])
        if start is not None:
            start_period = dateparser.parse(start)
        else:
            start_period = datetime.now().utcnow()

        if end is not None:
            end_period = dateparser.parse(end)
        else:
            cal = pdt.Calendar()
            diff = cal.parseDT(duration, sourceTime=datetime.min)[
                       0] - datetime.min
            end_period = start_period + diff

        utc = pytz.UTC

        start_period = utc.localize(start_period)
        end_period = utc.localize(end_period)

        parsed_matchers = helper.get_matchers_by_terms(matchers)
        self.log.info("Suppressing {0}->{1}".format(start_period, end_period))
        self.log.info("Matchers {0}".format(parsed_matchers))
        result = helper.post_silence(
            matchers=parsed_matchers,
            starts_at=start_period.isoformat(),
            ends_at=end_period.isoformat(),
            created_by=author,
            comment=comment
        )
        self.log.info("Added {0}".format(result))
        self.send_card(title="Silence added until {0}".format(end_period),
                    body="Alert created by {0} with description '{1}'. To cancel  !amtool silence expire {2}".format(author, comment, result.silence_id),
                    #                       thumbnail='https://raw.githubusercontent.com/errbotio/errbot/master/docs/_static/errbot.png',
                    #                       image='https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png',
                    # link=result["generatorURL"],
                    fields=helper.convert_matchers_to_tuples(parsed_matchers),
                    color='blue',
                    in_reply_to=mess)


    @arg_botcmd('silence_id', type=str)
    def amtool_silence_expire(self, mess, silence_id):
        """
             amtool silence expire silence-id

            expire an alertmanager silence

            Args:
              silence-id  Id of silences to expire
        """
        helper = AmtoolHelper(
            alertmanager_address=self.config['server_address'])
        result = helper.delete_silence(silence_id)
        return "Silence deleted"

    @arg_botcmd('--expired', action='store_true')
    @arg_botcmd('--within', type=str, default="")
    @arg_botcmd('matchers', type=str, metavar='matchers', nargs='+',
                template="amtool_silence_query")
    def amtool_silence_query(self, mess, expired=None, within=None, matchers=[]):
        """
          Amtool has a simplified prometheus query syntax The non-option section of arguments constructs a list of "Matcher Groups"
          that will be used to filter your query. The following examples will attempt to show this behaviour in action:

          amtool silence query alertname=foo node=bar

          This query will match all silences with the alertname=foo and node=bar label
          value pairs set.

          amtool silence query foo node=bar

          If alertname is omitted and the first argument does not contain a '=' or a
          '=~' then it will be assumed to be the value of the alertname pair.

          amtool silence query 'alertname=~foo.*'

          As well as direct equality, regex matching is also supported. The '=~' syntax
          (similar to prometheus) is used to represent a regex match. Regex matching
          can be used in combination with a direct match.

          In addition to filtering by silence labels, one can also query for silences that are due to expire soon
          with the "--within" parameter. In the event that you want to preemptively act upon expiring silences by
          either fixing them or extending them. For example:

          amtool silence query --within 8h

          returns all the silences due to expire within the next 8 hours. This syntax can also be combined with the label based
          filtering above for more flexibility.

          The "--expired" parameter returns only expired silences. Used in combination with "--within=TIME", amtool returns
          the silences that expired within the preceding duration.

          amtool silence query --within 2h --expired

returns all silences that expired within the preceeding 2 hours.

      --expired        Show expired silences instead of active
      --within=WITHIN  Show silences that will expire or have expired within a duration
        """
        helper = AmtoolHelper(
            alertmanager_address=self.config['server_address'])
        filters = helper.get_filters_by_terms(matchers)
        self.log.info("Expired {0} within {1} filtered {2}".format(expired, within, filters))
        result = helper.get_silences(filter=filters, expired=expired, within=within)
        return {"silences": result}
