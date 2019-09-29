import time
import numpy as np
import requests
from .base_crawler import BaseCrawler


def RandomSamplingApkCrawler(BaseCrawler):

    def __init__(self, sampling_num=100):
        super(RandomSamplingApkCrawler, self).__init__()
        self._MAX_FAIL_TOLERANCE = 1000
        self._APK_URL_FMT =  'https://www.apkmirror.com/wp-content/themes/APKMirror/download.php?id={_id}'
        self._SAMPLING_NUM = sampling_num
        self._ZIP_MAGIC = 'PK\x03\x04'

    def _crawl(self):
        success_num = 0
        fail_cnt = 0

        while success_num < self._SAMPLING_NUM:
            random_id = self._get_random_id()
            r = requests.get(
                self._APK_URL_FMT.format(_id=random_id),
                allow_redirects=True
            )

            if not self._validate_apk(r.content[:4].decode('utf-8')):
                fail_cnt += 1
                if fail_cnt >= self._MAX_FAIL_TOLERANCE:
                    break
                continue

            apk_filepath = f'/tmp/apkmirror_{random_id}.apk'
            with open(apk_filepath, 'wb') as f:
                f.write(r.content)

            success_num += 1
            yield apk_filepath

            if success_num >= self._SAMPLING_NUM:
                break

            time.sleep(3.0*np.random.rand())

    def _get_random_id(self):
        return np.random.randint(1000, 5000000)

    def _validate_apk(
        self,
        magic: str
    ):
        return magic == self._ZIP_MAGIC
