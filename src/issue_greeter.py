import asyncio
import os
import sys
import traceback
import aiohttp
from aiohttp import web
from gidgethub import aiohttp as gh_aiohttp
from gidgethub import routing
from gidgethub import sansio
from gidgethub import apps

router = routing.Router()

############################ Issue Greetings #############################################


@router.register("issues", action="opened")
async def issue_opened_event(event, gh, *args, **kwargs):

    installation_id = event.data["installation"]["id"]

    installation_access_token = await apps.get_installation_access_token(
        gh,
        installation_id=installation_id,
        app_id=os.environ.get("GH_APP_ID"),
        private_key=os.environ.get("GH_PRIVATE_KEY")
    )

    #url for the comment url
    url = event.data['issue']['comments_url']
    
    #author of the issue creator
    author = event.data['issue']['user']['login']
    
    #avatar url of the issue creator
    avatar = event.data['issue']['user']['avatar_url']

    message = f"<br><table><tbody><tr><td>Thanks for opening the issue @{author}! I will look into it ASAP!\n Till then show your love by staring my repos 😋<br>Please assign this issue to you by commenting `/assign`.</td><td> <img alt='Coding' width='100px' height='100px' src='{avatar}'></td></tr></tbody></table>"
    await gh.post(url, data={
        'body': message,
        },
        oauth_token=installation_access_token["token"]
                 )
