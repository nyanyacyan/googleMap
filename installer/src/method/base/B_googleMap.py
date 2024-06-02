# coding: utf-8
# ----------------------------------------------------------------------------------
# 2023/5/8更新

# ----------------------------------------------------------------------------------

import requests
import const
import json

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

    def _google_map_api_request(self, api_key, query):
        try:
            self.logger.info(f"******** google_map_api_request 開始 ********")
            url = const.endpoint_url

            params = {
                'query' : query,  # 検索ワード
                'key' : api_key
            }

            response = requests.get(url, params=params)

            if response.status_code == 200:
                json_data = response.json()
                return json_data

            elif response.status_code == 500:
                self.logger.error(f"google_map_api_request サーバーエラー")

            else:
                self.logger.error(f"google_map_api_request リクエストした際にエラーが発生")
                return None

            self.logger.info(f"******** google_map_api_request 終了 ********")


        except Exception as e:
            self.logger.error(f"google_map_api_request 処理中にエラーが発生: {e}")


# ----------------------------------------------------------------------------------
# jsonファイルの全ての中身を確認

    def _response_result_checker(self, json_data):
        try:
            self.logger.info(f"******** response_result_checker 開始 ********")

            if json_data:
                self.logger.warning(json.dumps(json_data, indent=2, ensure_ascii=False))

            else:
                raise Exception("json_data データがなし")

            self.logger.info(f"******** response_result_checker 終了 ********")


        except Exception as e:
            self.logger.error(f"response_result_checker 処理中にエラーが発生: {e}")


# ----------------------------------------------------------------------------------
# jsonファイルの特定のcolumnの内容を確認

    def _json_column(self, json_data, column):
        try:
            self.logger.info(f"******** _json_column 開始 ********")

            self.logger.debug(f"column:{column}")

            # jsonファイルが存在確認
            if not json_data:
                raise ValueError("json_data がNoneです")

            # jsonファイルに指定したcolumnがあるのか確認
            if column in json_data:
                raise KeyError(f"column '{column}' が JSONデータに存在しません")

            column_value = json_data[column]

            self.logger.warning(f"column_value: {column_value}")

            self.logger.info(f"******** _json_column 終了 ********")

            return column_value


        except KeyError as ke:
            self.logger.error(f"指定されたカラムにエラーがあります: {ke}")

        except ValueError as ve:
            self.logger.error(f"指定したcolumnのデータが指定したJSONファイルにない: {ve}")

        except Exception as e:
            self.logger.error(f"response_result_checker 処理中にエラーが発生: {e}")


# ----------------------------------------------------------------------------------
