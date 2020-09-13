# TradeCore Assignment

The assignment is published without the database, so you need to run the migration before use.

There is not much in terms of documentation or tests, because it was tedious to do as is. You might want to reconcider the scope of the assignment.

## Blog platform

**Important!** Because the specified Hunter and Clearbit require a phone number to use, I don't use them. There are placeholders in `serializers.py` and `models.py` for where their usage would be placed.

Django development configuration is used.

The API is built around [Django REST Framework](https://www.django-rest-framework.org/).

User managment API is managed via [Djoser](https://github.com/sunscrapers/djoser), and the JWT is powered by [Simple JWT](https://github.com/SimpleJWT/django-rest-framework-simplejwt). While JWT auth is supported, session auth is left active (for active users) as well, because the API browsers I use don't support JWT dynamic generation. If it's an issue, you can remove `'rest_framework.authentication.SessionAuthentication'` from `REST_FRAMEWORK`, `DEFAULT_AUTHENTICATION_CLASSES` in `settings.py`.

Default user model was not modified. For simplification, all the APIs require a user to use.

## Bot

The bot is designed using Requests.
The usernames that the bot is using are predetermined, so after the first run, no new users will be created. Results may vary.

The bot takes random words from here `http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain` and requires internet connection to function.

Use by running `python bot.py`.