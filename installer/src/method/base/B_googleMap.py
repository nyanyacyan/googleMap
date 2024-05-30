# coding: utf-8
# ----------------------------------------------------------------------------------
# 2023/5/8更新

# ----------------------------------------------------------------------------------

import requests
import const

# 自作モジュール
from .utils import Logger, NoneChecker

###############################################################
# googleMapApiを使ってrequest

class GoogleMapBase:
    def __init__(self, debug_mode=False):

        # logger
        self.setup_logger = Logger(__name__, debug_mode=debug_mode)
        self.logger = self.setup_logger.setup_logger()

        # noneチェック
        self.none = NoneChecker()


###############################################################
# ----------------------------------------------------------------------------------
# Google mapAPIへのrequest

    def google_map_api_request(self, api_key, query):
        try:
            self.logger.info(f"******** google_map_api_request 開始 ********")
            url = const.endpoint_url

            params = {
                'query' : query,
                'key' : api_key
            }


            response = requests.get(url, params=params)

            if response.status_code == 200:
                data = response.json()
                return data

            elif response.status_code == 500:
                self.logger.error(f"google_map_api_request サーバーエラー")


            self.logger.info(f"******** google_map_api_request 開始 ********")

        except Exception as e:
            self.logger.error(f"google_map_api_request 処理中にエラーが発生: {e}")


# ----------------------------------------------------------------------------------
