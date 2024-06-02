# coding: utf-8
# ----------------------------------------------------------------------------------
# 2023/5/8更新

# ----------------------------------------------------------------------------------

import time
import requests
import const
import json
import pandas as pd

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
            endpoint_url = const.endpoint_url

            params = {
                'query' : query,  # 検索ワード
                'key' : api_key
            }

            response = requests.get(endpoint_url, params=params, timeout=10)

            if response.status_code == 200:
                json_data = response.json()
                self.logger.info(f"******** google_map_api_request 終了 ********")
                return json_data

            elif response.status_code == 500:
                self.logger.error(f"google_map_api_request サーバーエラー")

            else:
                self.logger.error(f"google_map_api_request リクエストした際にエラーが発生: {response.status_code} - {response.text}")


            self.logger.info(f"******** google_map_api_request 終了 ********")

        except requests.exceptions.Timeout:
            self.logger.error(f"google_map_api_request リクエストでのタイムアウトエラー")

        except requests.exceptions.RequestException as e:
            self.logger.error(f"google_map_api_request リクエストエラーが発生: {e}")

        except Exception as e:
            self.logger.error(f"google_map_api_request 処理中にエラーが発生: {e}")

        finally:
            self.logger.info(f"******** google_map_api_request 終了 ********")

        return None


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
# 取得したjsonデータを再リクエストしなくて済むようにデータに置き換える


    def _get_json_to_dataframe(self, json_data):
        try:
            self.logger.info(f"******** _get_json_to_dataframe 開始 ********")

            # json_dataの中身を確認
            self._response_result_checker(json_data=json_data)

            # json_dataの「results」部分を抜き出す
            places = json_data.get('results', [])

            # jsonデータをDataFrameに変換
            df = pd.json_normalize(places)

            self.logger.debug(df.head())

            return df

        except Exception as e:
            self.logger.error(f"_get_json_to_dataframe 処理中にエラーが発生: {e}")


# ----------------------------------------------------------------------------------
# DataFrameから複数のcolumnの値データを取得する
#! columnsで必要なcolumnを順番に指定する
#! →columns = ["name", "geometry.location.lat", "geometry.location.lng", "rating"]

    def get_column_data_in_df(self, df, columns):
        try:
            self.logger.info(f"******** get_column_data_in_df 開始 ********")

            store_data_list = []

            if df:
                # iterrowsは一つずつ取り出す→Indexとデータをタプルで返す
                for index, row in df.iterrows():
                    # rowのデータからcolumnのデータをリストに入れ込んでいく
                    store_data = [row[column] for column in columns]

                    self.logger.info(f"store_data: {index} {store_data}")

                    store_data_list.append(store_data)

            else:
                self.logger.error(f"dfがNoneになっている")

            self.logger.info(f"store_data_list: \n{store_data_list}")

            self.logger.info(f"******** get_column_data_in_df 終了 ********")

            return store_data_list

        except Exception as e:
            self.logger.error(f"get_column_data_in_df 処理中にエラーが発生: {e}")


# ----------------------------------------------------------------------------------
# jsonファイルの特定のcolumnの内容を確認

    def _get_json_column_only_data(self, json_data, column):
        try:
            self.logger.info(f"******** _json_column 開始 ********")

            self.logger.debug(f"column:{column}")

            # jsonファイルが存在確認
            if not json_data:
                raise ValueError("json_data がNoneです")

            # jsonファイルに指定したcolumnがあるのか確認
            if column in json_data:
                raise KeyError(f"column '{column}' が JSONデータに存在しません")

            # jsonファイルの中にある'results'の中からデータを抜く
            places = json_data.get('results', [])

            for place in places:

                # columnごとの値
                column_value = place.get(column)

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
# jsonファイルの特定の階層がある部分の値を取得

    def _get_json_column_hierarchy_data(self, json_data, column, column2, column3):
        try:
            self.logger.info(f"******** response_result_checker 開始 ********")

            self.logger.debug(f"columns: {column}, {column2}, {column3}")

            if not json_data:
                raise ValueError("json_data がNoneです")


            # jsonファイルの中にある'results'の中からデータを抜く
            places = json_data.get('results', [])

            for place in places:
                if column in place and column2 in place[column] and column3 in place[column][column2]:

                # columnごとの値
                    column_value = place[column][column2][column3]

                else:
                    raise KeyError(f"指定したcolumn '{column}/{column2}/{column3}'が jsonデータに存在しない")

            self.logger.warning(f"column_value: {column_value}")

            self.logger.info(f"******** response_result_checker 終了 ********")

            return column_value


        except KeyError as ke:
            self.logger.error(f"指定されたカラムにエラーがあります: {ke}")

        except ValueError as ve:
            self.logger.error(f"指定したcolumnのデータが指定したJSONファイルにない: {ve}")

        except Exception as e:
            self.logger.error(f"response_result_checker 処理中にエラーが発生: {e}")

# ----------------------------------------------------------------------------------
# place_idを取得

    def _get_place_id(self, json_data):
        try:
            self.logger.info(f"******** _get_place_id 開始 ********")

            if not json_data:
                raise ValueError("json_data がNoneです")

            # jsonファイルの中にある'results'の中からデータを抜く
            places = json_data.get('results', [])

            for place in places:

                # columnごとの値
                plase_id_value = place.get('plase_id')

            self.logger.warning(f"column_value: {plase_id_value}")

            self.logger.info(f"******** _get_place_id 終了 ********")

            return plase_id_value


        except KeyError as ke:
            self.logger.error(f"指定されたカラムにエラーがあります: {ke}")

        except ValueError as ve:
            self.logger.error(f"指定したcolumnのデータが指定したJSONファイルにない: {ve}")

        except Exception as e:
            self.logger.error(f"_get_place_id 処理中にエラーが発生: {e}")


# ----------------------------------------------------------------------------------
# plase_idを使ってrequestをして詳細情報を取得

    def _plase_id_request(self, api_key, place_id):
        try:
            self.logger.info(f"******** _plase_id_request 開始 ********")
            endpoint_url = const.endpoint_url

            params = {
                'place_id' : place_id,  # IDによる詳細情報を取得
                'key' : api_key
            }

            response = requests.get(endpoint_url, params=params, timeout=10)

            # ステータスコードが成功ならjsonを返す
            if response.status_code == 200:
                json_data = response.json()

                self.logger.info(f"******** _plase_id_request 終了 ********")

                return json_data


            elif response.status_code == 500:
                self.logger.error(f"_plase_id_request サーバーエラー")

            else:
                self.logger.error(f"_plase_id_request リクエストした際にエラーが発生: {response.status_code} - {response.text}")


            self.logger.info(f"******** _plase_id_request 終了 ********")

        except requests.exceptions.Timeout:
            self.logger.error(f"_plase_id_request リクエストでのタイムアウトエラー")

        except requests.exceptions.RequestException as e:
            self.logger.error(f"_plase_id_request リクエストエラーが発生: {e}")

        except Exception as e:
            self.logger.error(f"_plase_id_request 処理中にエラーが発生: {e}")

        finally:
            self.logger.info(f"******** _plase_id_request 終了 ********")

        return None


# ----------------------------------------------------------------------------------
# Google mapAPIでjson取得
# jsonからplase_idを取得
# plase_idから詳細が掲載されてるjsonを取得
# jsonからDataFrameへ変換
# DataFrameから行ごとのデータをリストへ変換する

    def get_gm_df_list(self, api_key, query, columns):
        try:
            self.logger.info(f"******** get_gm_df_list 開始 ********")

            # gmAPIリクエスト
            json_data = self._google_map_api_request(api_key=api_key, query=query)
            time.sleep(2)

            # plase_idを取得
            plase_id = self._get_place_id(json_data=json_data)
            time.sleep(2)

            # 詳細データを取得
            details_data = self._plase_id_request(api_key=api_key, place_id=plase_id)
            time.sleep(2)

            # 詳細データをDataFrameに変換
            df = self._get_json_to_dataframe(json_data=details_data)
            time.sleep(2)

            # DataFrameから必要なcolumn情報を取得
            self.get_column_data_in_df(df=df, columns=columns)
            time.sleep(2)



            self.logger.info(f"******** get_gm_df_list 終了 ********")

        except Exception as e:
            self.logger.error(f"get_gm_df_list 処理中にエラーが発生: {e}")


