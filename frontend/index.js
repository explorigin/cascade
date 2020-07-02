function connectToSubscription(event) {
    event.preventDefault()
    const el = document.getElementById("subscriptionKey");
    if (!el.value) {
        return;
    }

    // FIXME: currently koa-proxies doesn't support websocket proxying so we access the api directly.
    ws = new WebSocket(`ws://localhost:8000/subscriptions/${el.value}/ws`);

    document.getElementById("connectForm").remove();
    document.querySelector('h1').innerText = `Monitoring ${el.value}`;

    el.value = '';

    ws.onmessage = function(event) {
        var messages = document.getElementById('messages')
        var message = document.createElement('li')
        var content = document.createTextNode(event.data)
        message.appendChild(content)
        messages.appendChild(message)
    };
}
