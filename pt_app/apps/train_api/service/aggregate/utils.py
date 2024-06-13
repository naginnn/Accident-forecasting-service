import datetime
import re
from apps.train_api.service.aggregate.config import ERRORS


class Utils:
    # Use in view, unprocessed
    @staticmethod
    def get_coord(x, darr=False):
        res = []
        if isinstance(x, str):
            numbers = re.findall(r'[\d\.\-]+', x)
            try:
                if darr:
                    tmp = []
                    for i in numbers:
                        tmp.append(float(i))
                        if len(tmp) == 2:
                            # tmp.reverse()
                            res.append(tmp)
                            tmp = []
                else:
                    res = [float(num) for num in numbers]
                    # res.reverse()
            except ValueError:
                return x
            else:
                return res
        else:
            return x

    # Not Used
    @staticmethod
    def collect_the_date(x):
        return datetime.datetime(int(x['year']), int(x['month']), int(x['day']))

    # Not used
    @staticmethod
    def get_error_desc(x):
        errs = []
        try:
            for err in x.split(','):
                errs.append(ERRORS.get(err, 'Нет данных'))
        finally:
            if errs:
                return ','.join(errs)
            else:
                return 'Нет данных'
