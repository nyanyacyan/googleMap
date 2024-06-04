# coding: utf-8
# ----------------------------------------------------------------------------------
# 2023/6/4更新

# ----------------------------------------------------------------------------------

import time

# 自作モジュール
from .base.B_googleMap import GoogleMapBase
from .base.utils import Logger

###############################################################


class GetGMPlaceDf(GoogleMapBase):
    def __init__(self, api_key, debug_mode=False):
        self.api_key = api_key

        # logger
        self.setup_logger = Logger(__name__, debug_mode=debug_mode)
        self.logger = self.setup_logger.setup_logger()


###############################################################
# ----------------------------------------------------------------------------------
# Override

    def _google_map_api_request(self, query):
        return super()._google_map_api_request(query)

    def _get_place_id(self, json_data):
        return super()._get_place_id(json_data)

    def _place_id_requests_in_list(self, place_id_list):
        return super()._place_id_requests_in_list(place_id_list)

    def _get_results_list(self, place_details_results_list):
        return super()._get_results_list(place_details_results_list)


# ----------------------------------------------------------------------------------
# GMのPlace APIへのリクエストしてdetail_dataを取得

    def process(self, query):
        try:
            self.logger.info(f"******** get_gm_df_list 開始 ********")

            # gmAPIリクエスト
            json_data = self._google_map_api_request(query=query)
            time.sleep(2)

            # plase_id_listを取得
            plase_id_list = self._get_place_id(json_data=json_data)
            time.sleep(2)

            # 詳細データを取得
            details_data_list = self._place_id_requests_in_list(place_id_list=plase_id_list)
            time.sleep(2)

            # 詳細データリストからresult部分を抽出してリストを作成
            results_data_list= self._get_results_list(place_details_results_list=details_data_list)
            time.sleep(2)


            # 詳細データをDataFrameに変換
            key_df = self._get_json_to_dataframe(json_data=results_data_list)
            time.sleep(2)

            self.logger.info(f"******** get_gm_df_list 終了 ********")

            return key_df

        except Exception as e:
            self.logger.error(f"get_gm_df_list 処理中にエラーが発生: {e}")


# ----------------------------------------------------------------------------------
