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
- `app_id` と `cert_id` に実際の値を設定してください
- 必要に応じてスコープを調整してください

トークンの使用上の注意:
- トークンは2時間（7,200秒）有効
- トークンは機密情報なので、公開しない
- 可能であれば、有効期間中はトークンを再利用
"""

import base64
import requests


class OAuthClient:
    """eBay OAuth Client"""

    def __init__(
        self, app_id: str, cert_id: str, dev_id: str, environment: str = "production"
    ):
        """
        eBay OAuth クライアント初期化
        Initialize eBay OAuth Client for obtaining access tokens

        :param app_id: eBay application ID
        :param cert_id: eBay certification ID
        :param dev_id: eBay developer ID
        :param environment: 'sandbox' または 'production'

        Not in use in this case.
        dev_id

        """
        self.app_id = app_id
        self.cert_id = cert_id
        self.dev_id = dev_id

        # 環境に応じたエンドポイント設定
        if environment.lower() == "sandbox":
            self.token_endpoint = (
                "https://api.sandbox.ebay.com/identity/v1/oauth2/token"
            )
        else:
            # eBay production OAuth endpoints
            self.token_endpoint = "https://api.ebay.com/identity/v1/oauth2/token"

        # Base64エンコードされた認証情報の生成
        credentials = f"{self.app_id}:{self.cert_id}"
        self.encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode(
            "utf-8"
        )

        # Scopes for Browse API
        self.scopes = [
            # eBayの公開データを見る
            "https://api.ebay.com/oauth/api_scope",
            "https://api.ebay.com/oauth/api_scope/buy.browse",
            "https://api.ebay.com/oauth/api_scope/buy.item.bulk",
            # 広告キャンペーンや出品プロモーションなどのeBayマーケティング活動を表示します
            "https://api.ebay.com/oauth/api_scope/sell.marketing.readonly",
            # 広告キャンペーンや出品プロモーションなどのeBayマーケティング活動を表示および管理します
            "https://api.ebay.com/oauth/api_scope/sell.marketing",
            # 在庫とオファーを表示する
            "https://api.ebay.com/oauth/api_scope/sell.inventory.readonly",
            # 在庫とオファーを表示および管理する
            "https://api.ebay.com/oauth/api_scope/sell.inventory",
            # アカウント設定を表示する
            "https://api.ebay.com/oauth/api_scope/sell.account.readonly",
            # アカウント設定の表示と管理
            "https://api.ebay.com/oauth/api_scope/sell.account",
            # 注文の履行状況を確認する
            "https://api.ebay.com/oauth/api_scope/sell.fulfillment.readonly",
            # 注文の履行状況を表示および管理する
            "https://api.ebay.com/oauth/api_scope/sell.fulfillment",
            # パフォーマンスレポートなどの販売分析データを表示する
            "https://api.ebay.com/oauth/api_scope/sell.analytics.readonly",
            # 支払い情報と注文情報を表示および管理し、この情報を表示して、サードパーティのアプリケーションを使用して払い戻しを開始できるようにします。
            "https://api.ebay.com/oauth/api_scope/sell.finances",
            # 紛争および関連する詳細（支払いおよび注文情報を含む）を表示および管理します。
            "https://api.ebay.com/oauth/api_scope/sell.payment.dispute",
            # eBay メンバーアカウントからユーザー名やビジネスアカウントの詳細などのユーザーの基本情報を表示します。
            "https://api.ebay.com/oauth/api_scope/commerce.identity.readonly",
            # フィードバックなどの評判データを表示および管理します。
            # "https://api.ebay.com/oauth/api_scope/sell.reputation",
            # フィードバックなどの評判データを表示します。
            "https://api.ebay.com/oauth/api_scope/sell.reputation.readonly",
            # イベント通知サブスクリプションの表示と管理
            "https://api.ebay.com/oauth/api_scope/commerce.notification.subscription",
            # イベント通知のサブスクリプションを表示する
            "https://api.ebay.com/oauth/api_scope/commerce.notification.subscription.readonly",
            # eBayストアの表示と管理
            "https://api.ebay.com/oauth/api_scope/sell.stores",
            # eBayストアを見る
            "https://api.ebay.com/oauth/api_scope/sell.stores.readonly",
            # 購入者への商品のマーケティングに使用するために、eBay の商品と出品データを取得します。
            "https://api.ebay.com/oauth/api_scope/buy.marketing	",
        ]

    def get_application_token(self) -> tuple[str, int, str] | None:
        # def get_application_token(self) -> dict[str, str] | None:
        """
        アプリケーションアクセストークンの取得

        :param scopes: スコープのリスト
        :return: アクセストークン情報の辞書

        返却値は以下のような内容となる
        {'access_token': "トークン文字列",
         'expires_in': 7200,
         'token_type': 'Application Access Token'
        }
        """
        # リクエストヘッダー
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {self.encoded_credentials}",
        }

        # リクエストボディ
        payload = {"grant_type": "client_credentials", "scope": self.scopes}

        try:
            # トークンエンドポイントにPOSTリクエスト
            response = requests.post(self.token_endpoint, headers=headers, data=payload)

            # レスポンスのチェック
            response.raise_for_status()

            info = response.json()
            access_token = info.get("access_token")
            expires_in: int = info.get("expires_in")
            token_type = info.get("token_type")

            # トークン情報を返す
            return access_token, expires_in, token_type

        except requests.exceptions.RequestException as e:
            print(f"Error obtaining token: {e}")
            return None


def main():
    import config
    # アプリケーションID、証明書ID、開発者ID、トークン、セラー名
    APP_ID = config.APP_ID
    CERT_ID = config.CERT_ID
    DEV_ID = config.DEV_ID

    # eBay OAuth クライアントの初期化
    oauth = OAuthClient(
        app_id=APP_ID, cert_id=CERT_ID, dev_id=DEV_ID, environment="production"
    )
    token_info = oauth.get_application_token()
    if token_info:
        print(token_info[0])
        print("-" * 10)
        print(token_info[1])
        print("-" * 10)
        print(token_info[2])
    else:
        print("Failed to get token")


if __name__ == "__main__":
    main()
