"""
eBayのOAuth Client Credentials Grant Flowを使用してトークンを取得するPythonコードを作成します。

このPythonスクリプトは、eBayのOAuth Client Credentials Grant Flowを実装しています。

主な特徴は以下の通りです：

1. `eBayOAuthClient`クラスを使用して、トークン取得プロセスをカプセル化
2. サンドボックスと本番環境の両方のエンドポイントをサポート
3. Base64エンコーディングされた認証情報の自動生成
4. スコープのURL エンコーディング
5. エラーハンドリングと例外処理
6. 簡単にカスタマイズ可能な `main()` 関数

使用する際の注意点:
- `client_id` と `client_secret` に実際の値を設定してください
- 必要に応じてスコープを調整してください
- 必要な `requests` ライブラリをインストールしてください (`pip install requests`)

トークンの使用上の注意:
- トークンは2時間（7,200秒）有効です
- トークンは機密情報なので、公開しないでください
- 可能であれば、有効期間中はトークンを再利用してください

何か質問や modification が必要でしたら、お知らせください。
"""
import base64
import requests

import config


class eBayOAuthClient:
    def __init__(self, client_id: str, client_secret: str, environment='sandbox'):
        """
        eBay OAuth クライアント初期化
        
        :param client_id: アプリケーションのクライアントID
        :param client_secret: アプリケーションのクライアントシークレット
        :param environment: 'sandbox' または 'production'
        """
        self.client_id: str = client_id
        self.client_secret: str = client_secret
        
        # 環境に応じたエンドポイント設定
        if environment.lower() == 'sandbox':
            self.token_endpoint = 'https://api.sandbox.ebay.com/identity/v1/oauth2/token'
        else:
            self.token_endpoint = 'https://api.ebay.com/identity/v1/oauth2/token'
        
        # Base64エンコードされた認証情報の生成
        credentials = f"{self.client_id}:{self.client_secret}"
        self.encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

        
    # def get_application_token(self, scopes):
    def get_application_token(self):
        """
        アプリケーションアクセストークンの取得
        
        :param scopes: スコープのリスト
        :return: アクセストークン情報の辞書
        """
        scopes = [
            # eBayの公開データを見る
            "https://api.ebay.com/oauth/api_scope",
            "https://api.ebay.com/oauth/api_scope/buy.item.bulk",
            "https://api.ebay.com/oauth/api_scope/sell.marketing.readonly",
            "https://api.ebay.com/oauth/api_scope/sell.marketing",
            "https://api.ebay.com/oauth/api_scope/sell.inventory.readonly",
            "https://api.ebay.com/oauth/api_scope/sell.inventory",
            "https://api.ebay.com/oauth/api_scope/sell.account.readonly",
            "https://api.ebay.com/oauth/api_scope/sell.account",
            "https://api.ebay.com/oauth/api_scope/sell.fulfillment.readonly",
            "https://api.ebay.com/oauth/api_scope/sell.fulfillment",
            "https://api.ebay.com/oauth/api_scope/sell.analytics.readonly",
            "https://api.ebay.com/oauth/api_scope/sell.finances",
            "https://api.ebay.com/oauth/api_scope/sell.payment.dispute",
            "https://api.ebay.com/oauth/api_scope/commerce.identity.readonly",
            "https://api.ebay.com/oauth/api_scope/sell.reputation",
            "https://api.ebay.com/oauth/api_scope/sell.reputation.readonly",
            "https://api.ebay.com/oauth/api_scope/commerce.notification.subscription",
            "https://api.ebay.com/oauth/api_scope/commerce.notification.subscription.readonly",
            "https://api.ebay.com/oauth/api_scope/sell.stores",
            "https://api.ebay.com/oauth/api_scope/sell.stores.readonly"
            # 購入者への商品のマーケティングに使用するために、eBay の商品と出品データを取得します。
            "https://api.ebay.com/oauth/api_scope/buy.marketing	"
        ]

        # リクエストヘッダー
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Basic {self.encoded_credentials}'
        }
        
        # リクエストボディ
        payload = {
            'grant_type': 'client_credentials',
            'scope': scopes
        }
        
        try:
            # トークンエンドポイントにPOSTリクエスト
            response = requests.post(
                self.token_endpoint, 
                headers=headers, 
                data=payload
            )
            
            # レスポンスのチェック
            response.raise_for_status()
            
            # トークン情報を返す
            return response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"Error obtaining token: {e}")
            return None


def get_fresh_token(debug=False) -> str | None:
    client_id = config.APP_ID
    client_secret = config.CERT_ID
    
    # eBayオブジェクトの作成
    ebay_client = eBayOAuthClient(client_id, client_secret, environment="production")
    
    # トークンの取得
    token_response = ebay_client.get_application_token()
    # token_response = ebay_client.get_application_token(scopes)
    
    if token_response:
        fresh_token: str = token_response['access_token']
        if debug:
            print("Access Token:", fresh_token)
            print("Expires in:", token_response['expires_in'], "seconds")
        return fresh_token
    else:
        print("Token retrieval failed")


def main():
    fresh_token: str | None = get_fresh_token()
    if fresh_token:
        print("Access Token:", fresh_token)


if __name__ == '__main__':
    main()
