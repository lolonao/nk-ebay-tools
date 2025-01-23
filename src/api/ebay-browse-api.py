"""
動作する。トークンは毎回取得
"""

import requests

# import time
import json
from typing import Dict, List, Optional
# from typing import Union

import config

# 毎回トークンを取得する
import ebay_oauth_token


class EbayOAuthClient:
    def __init__(self, app_id: str, cert_id: str, dev_id: str):
        """
        Initialize eBay OAuth Client for obtaining access tokens

        :param app_id: eBay application ID
        :param cert_id: eBay certification ID
        :param dev_id: eBay developer ID
        """
        self.app_id = app_id
        self.cert_id = cert_id
        # self.dev_id = dev_id

        # eBay production OAuth endpoints
        self.auth_url = "https://api.ebay.com/identity/v1/oauth2/token"

        # Scopes for Browse API
        self.scope = "https://api.ebay.com/oauth/api_scope/buy.browse"

    def get_access_token(self) -> str | None:
        """
        Obtain OAuth 2.0 access token using client credentials flow

        :return: Access token string
        """
        try:
            import ebay_oauth_token

            AUTH_TOKEN = ebay_oauth_token.get_fresh_token()
            return AUTH_TOKEN

        except requests.RequestException as e:
            print(f"Token Request Error: {e}")
            print(
                f"Response Content: {e.response.text if hasattr(e, 'response') else 'No response'}"
            )
            raise


class EbayBrowseAPI:
    # def __init__(self, app_id: str, cert_id: str, dev_id: str, auth_token: str):
    def __init__(self, app_id: str, cert_id: str, dev_id: str):
        """
        Initialize eBay Browse API client with OAuth authentication

        :param app_id: eBay application ID
        :param cert_id: eBay certification ID
        :param dev_id: eBay developer ID
        :param auth_token: eBay authentication token
        """
        self.oauth_client = EbayOAuthClient(app_id, cert_id, dev_id)
        self.base_url = "https://api.ebay.com/buy/browse/v1/item_summary/search"

        # Get fresh access tokenBaaS
        access_token = self.oauth_client.get_access_token()

        # Construct headers with token
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "X-EBAY-C-MARKETPLACE-ID": "EBAY_US",
        }

        # # Construct headers with token
        # self.headers = {
        #     "Authorization": f"Bearer {access_token}",
        #     "Content-Type": "application/json",
        #     "X-EBAY-C-MARKETPLACE-ID": "EBAY_US",
        # }

    def search(
        self,
        q: Optional[str] = None,
        category_ids: Optional[str] = None,
        gtin: Optional[str] = None,
        filter_fields: Optional[List[str]] = None,
        sort: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
        aspect_filter: Optional[Dict] = None,
        compatibility_filter: Optional[Dict] = None,
        auto_correct: bool = False,
        fieldgroups: Optional[str] = None,
    ) -> Dict:
        """
        Search for items on eBay with dynamic token retrieval

        :param q: Search query string
        :param category_ids: Comma-separated list of category IDs
        :param gtin: Global Trade Item Number
        :param filter_fields: List of filter fields
        :param sort: Sort order
        :param limit: Maximum number of items to return (max 200)
        :param offset: Pagination offset
        :param aspect_filter: Aspect filter dictionary
        :param compatibility_filter: Compatibility filter dictionary
        :param auto_correct: Enable auto-correction
        :param fieldgroups: Field groups to include
        :return: Search results dictionary

        """
        # # Get fresh access tokenBaaS
        # access_token = self.oauth_client.get_access_token()
        #
        # # Construct headers with token
        # headers = {
        #     "Authorization": f"Bearer {access_token}",
        #     "Content-Type": "application/json",
        #     "X-EBAY-C-MARKETPLACE-ID": "EBAY_US",
        # }

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
            print(
                f"Response Content: {e.response.text if hasattr(e, 'response') else 'No response'}"
            )
            return {}

    def get_item_details(self, item_id: str) -> Dict:
        """
        Retrieve detailed information for a specific item

        :param item_id: eBay item ID
        :return: Item details dictionary
        """
        item_url = f"https://api.ebay.com/buy/browse/v1/item/{item_id}"

        try:
            response = requests.get(item_url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Item Details Request Error: {e}")
            return {}


# 商品詳細情報
def print_detail_info(item_info: dict):
    print(item_info.get("itemId"))

    print(item_info.get("sellerItemRevision"))
    print(item_info.get("title"))
    print(item_info.get("shortDescription"))
    print(item_info.get("price"))
    print(item_info.get("categoryPath"))

    print(item_info.get("categoryIdPath"))
    print(item_info.get("condition"))
    print(item_info.get("conditionId"))
    print(item_info.get("itemLocation"))
    print(item_info.get("image"))
    print(item_info.get(""))
    print(item_info.get(""))


def main():
    # Replace these with your actual credentials
    APP_ID = config.APP_ID
    CERT_ID = config.CERT_ID
    DEV_ID = config.DEV_ID
    # AUTH_TOKEN = config.TOKEN

    # Initialize eBay Browse API client
    ebay_api = EbayBrowseAPI(APP_ID, CERT_ID, DEV_ID)

    try:
        # Example search for smartphones
        search_results = ebay_api.search(
            # q=r"Apple",
            # q=r"Solomon+Studio+1%2F100+RX-78GP02A+Gundam+Physalis",
            q=r"RX-78GP02A+Gundam+Physalis",
            # category_ids='9355',  # Electronics category
            filter_fields=[
                "price:[50..500]",  # Price range filter
                "condition:{NEW|USED}",  # Condition filterBaaS
                "sellers:ayumi.kur_89",
                "priceCurrency:USD",
            ],
            limit=10,
            # sort="price",
            sort="newlyListed",
        )

        # Print search results
        if search_results and "itemSummaries" in search_results:
            print("取得できる項目")
            for i in search_results:
                print(i)

            print("*" * 50)

            for item in search_results["itemSummaries"]:
                print(f"Title: {item.get('title', 'N/A')}")
                print(
                    f"Price: {item.get('price', {}).get('value', 'N/A')} {item.get('price', {}).get('currency', '')}"
                )
                print(f"Item URL: {item.get('itemWebUrl', 'N/A')}")
                print(f"watch count: {item.get('watchCount', 'N/A')}")
                print(f"watch count: {item.get('unitPricingMeasure', 'N/A')}")

                print("-" * 50)

            # 1件目の商品詳細情報
            first_item_id = search_results["itemSummaries"][0].get("itemId")
            if first_item_id:
                item_details = ebay_api.get_item_details(first_item_id)
                print_detail_info(item_details)
                # print("最初の商品詳細情報:", json.dumps(item_details, indent=2))

        else:
            print("No items found or error in search results")
            print(json.dumps(search_results, indent=2))

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
