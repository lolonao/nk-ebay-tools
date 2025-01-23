"""
eBay Browse API Client
This client will get the access token from eBay OAuth API each time.
"""

import requests
import json
from typing import Any, Dict

import config
from oauth_client import OAuthClient 

class EbayBrowseAPIClient:
    BASE_URL = "https://api.ebay.com/buy/browse/v1"
    def __init__(self, app_id: str, cert_id: str, dev_id: str):
        """
        Initialize eBay Browse API client with OAuth authentication

        :param app_id: eBay application ID
        :param cert_id: eBay certification ID
        :param dev_id: eBay developer ID
        """
        self.base_url = "https://api.ebay.com/buy/browse/v1/item_summary/search"
        # self.BASE_URL = "https://api.ebay.com/buy/browse/v1"
        # self.oauth_client = oauth_client.OAuthClient(app_id, cert_id, dev_id)
        self.oauth = OAuthClient(app_id, cert_id, dev_id, "production")
        self.token_response = self.oauth.get_application_token()
        if self.token_response:
            self.token = self.token_response[0]
        else:
            print("Token retrieval failed")
            raise
        # self.token = self.get_token()
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            # デフォルトで米国のマーケットプレイスを使用
            "X-EBAY-C-MARKETPLACE-ID": "EBAY_US",
        }



    # def get_token(self):
    #     if self.token_response:
    #         a, b, c = self.token_response()
    #         fresh_token: str = self.token_response["access_token"]
    #         print("Access Token:", fresh_token)
    #         print("Expires in:", self.token_response["expires_in"], "seconds")
    #         return fresh_token
    #     else:
    #         print("Token retrieval failed")
    
    def search(
        self,
        q: str | None = None,
        category_ids: str | None = None,
        gtin: str | None = None,
        filter_fields: list[str] | None = None,
        sort: str | None = None,
        limit: int = 50,
        offset: int = 0,
        aspect_filter: dict | None = None,
        compatibility_filter: dict | None = None,
        auto_correct: bool = False,
        fieldgroups: str | None = None,
    ) -> dict:
        """
        Search for items on eBay with dynamic token retrieval
        """
        # Get fresh access token
        # access_token = self.oauth_client.get_access_token()

        # Construct headers with token
        # headers = {
        #     "Authorization": f"Bearer {self.token}",
        #     "Content-Type": "application/json",
        #     # デフォルトで米国のマーケットプレイスを使用
        #     "X-EBAY-C-MARKETPLACE-ID": "EBAY_US",
        # }
        #

        # Construct query parameters
        params = {"limit": str(limit), "offset": str(offset)}

        # Add optional parameters (same as previous implementation)
        if q:
            params["q"] = q
        if category_ids:
            params["category_ids"] = category_ids
        if gtin:
            params["gtin"] = gtin
        if filter_fields:
            params["filter"] = ",".join(filter_fields)
        if sort:
            params["sort"] = sort
        if aspect_filter:
            params["aspect_filter"] = json.dumps(aspect_filter)
        if compatibility_filter:
            params["compatibility_filter"] = json.dumps(compatibility_filter)
        if auto_correct:
            params["auto_correct"] = "true"
        if fieldgroups:
            params["fieldgroups"] = fieldgroups

        # Make the API request
        try:
            response = requests.get(self.base_url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"API Request Error: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response Content: {e.response.text}")
            raise

    def get_item(self, item_id: str) -> Dict[str, Any]:
        endpoint = f"{self.BASE_URL}/item/{item_id}"
        response = requests.get(endpoint, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    # def get_items_by_group(self, group_ids: list[str]) -> dict[str, Any]:
    #     endpoint = f"{self.BASE_URL}/item"
    #     params = {
    #         "item_group_ids": ",".join(group_ids)
    #     }
    #     response = requests.get(endpoint, headers=self._get_headers(), params=params)
    #     response.raise_for_status()
    #     return response.json()
    #



def main():
    # Replace these with your actual credentials
    APP_ID = config.APP_ID
    CERT_ID = config.CERT_ID
    DEV_ID = config.DEV_ID

    # Initialize eBay Browse API client
    # この時点でトークンは取得済み
    ebay_api = EbayBrowseAPIClient(APP_ID, CERT_ID, DEV_ID)
 
    try:
        # 検索条件の指定
        search_results = ebay_api.search(
            q="Gundam",
            category_ids="9355",  # Electronics category
            filter_fields=[
                "price:[50..500]",  # Price range filter
                "sellers:ayumi.kur_89",
                "priceCurrency:USD",
                "condition:{NEW|USED}",  # Condition filter
            ],
            limit=10,
            # sort="price",
            sort="newlyListed",
        )

        print(f"件数: {len(search_results)}")
        # Print search results
        if search_results and "itemSummaries" in search_results:
            print(f"nagasa: {len(search_results['itemSummaries'])}")
            for item in search_results["itemSummaries"]:
                print(f"Title: {item.get('title', 'N/A')}")
                print(
                    f"Price: {item.get('price', {}).get('value', 'N/A')} {item.get('price', {}).get('currency', '')}"
                )
                print(f"Item URL: {item.get('itemWebUrl', 'N/A')}")
                print("-" * 54)
        else:
            print("No items found or error in search results")
            print(json.dumps(search_results, indent=2))

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
