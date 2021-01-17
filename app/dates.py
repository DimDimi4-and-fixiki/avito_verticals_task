import datetime


class DateHandler(object):
    @staticmethod
    def check_date(date: str) -> bool:
        """
        Checks if date is valid
        Date is in format "YYYY-MM-DD"
        :return: True if date is valid; False if not
        """
        y, m, d = map(int, date.split("-"))
        try:  # Tries to make a date
            res = datetime.date(y, m, d)
            print(y, m, d)
        except ValueError:  # Couldn't make a date
            return False

        return True
