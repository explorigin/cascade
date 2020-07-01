
from fastapi import APIRouter
from starlette.responses import HTMLResponse


router = APIRouter()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>Monitor Subscription</h1>
        <form id="connectForm" action="" onsubmit="connectToSubscription(event)">
            <input type="text" id="subscriptionKey" autocomplete="off"/>
            <button>Connect</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            function connectToSubscription(event) {
                event.preventDefault()
                const el = document.getElementById("subscriptionKey");
                if (!el.value) {
                    return;
                }
                
                document.getElementById("connectForm").remove();
                document.querySelector('h1').innerText = `Monitoring ${el.value}`;
                
                ws = new WebSocket(`ws://localhost/subscriptions/${el.value}/ws`);
                ws.onmessage = function(event) {
                    var messages = document.getElementById('messages')
                    var message = document.createElement('li')
                    var content = document.createTextNode(event.data)
                    message.appendChild(content)
                    messages.appendChild(message)
                };
                el.value = '';
            }
        </script>
    </body>
</html>
"""


@router.get("/")
async def get():
    return HTMLResponse(html)
