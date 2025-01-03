from form_campaign_app import app
from form_campaign_app.setup import constant as const

if __name__ == "__main__":
    app.run(host=const.APP_HOST,
            port=const.APP_PORT,
            debug=bool(const.APP_DEBUG_BOOL),
            )
