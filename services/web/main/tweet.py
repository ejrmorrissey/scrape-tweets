from datetime import datetime, timedelta
import re


class Tweet:

    DAY_MONTH_FORMAT_STRING = "%b %d"
    FULL_DATE_FORMAT_STRING = "%b %d, %Y"

    DAY_MONTH_PATTERN = re.compile(r"^[A-Z][a-z]{2} \d{1,2}$")
    HOUR_PATTERN = re.compile(r"^\d{1,2}h$")
    MINUTE_PATTERN = re.compile(r"^\d{1,2}m$")
    SECOND_PATTERN = re.compile(r"^\d{1,2}s$")
    FULL_DATE_PATTERN = re.compile(r"^[A-Z][a-z]{2} \d{1,2}, \d{4}$")

    def __init__(self, status_id, account, date_string, text, pinned=False):
        self.status_id = status_id
        self.account = account
        self.date_string = date_string
        self.date = self._parse_date_string(date_string)
        self.text = text
        self.pinned = pinned

    @classmethod
    def from_json(cls, obj):
        status_id = obj["status"]
        account = obj["user"]
        text = obj["text"]
        date_string = obj["date"]
        return Tweet(status_id=status_id, account=account, date_string=date_string, text=text, pinned=False)

    def _parse_date_string(self, date_string):
        if self.DAY_MONTH_PATTERN.match(date_string):
            tweet_date = datetime.strptime(date_string, self.DAY_MONTH_FORMAT_STRING)\
                .replace(year=datetime.today().year)
            return tweet_date
        elif self.HOUR_PATTERN.match(date_string):
            current_datetime = datetime.today()
            hour_delta = timedelta(hours=int(date_string.replace("h", "")))
            tweet_date = current_datetime - hour_delta
            return tweet_date
        elif self.FULL_DATE_PATTERN.match(date_string):
            tweet_date = datetime.strptime(date_string, self.FULL_DATE_FORMAT_STRING)
            return tweet_date
        elif self.MINUTE_PATTERN.match(date_string):
            current_datetime = datetime.today()
            minute_delta = timedelta(minutes=int(date_string.replace("m", "")))
            tweet_date = current_datetime - minute_delta
            return tweet_date
        elif self.SECOND_PATTERN.match(date_string):
            current_datetime = datetime.today()
            second_delta = timedelta(seconds=int(date_string.replace("s", "")))
            tweet_date = current_datetime - second_delta
            return tweet_date
        else:
            return None

    def as_text(self):
        return "\n".join([self.status_id, self.account, self.date.strftime(self.FULL_DATE_FORMAT_STRING), self.text])

    def as_text_with_date_string(self):
        return "\n".join([self.status_id, self.account, self.date_string, self.text])

    def as_dict(self):
        # This method is used when serialising tweets. We discard the original date string we scraped which might be
        # relative (e.g. 19h) and use an absolute date
        return {"status": self.status_id, "user": self.account,
                "date": self.date.strftime(self.FULL_DATE_FORMAT_STRING),
                "text": self.text, "date_string": self.date.strftime(self.FULL_DATE_FORMAT_STRING)}

