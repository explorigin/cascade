export function CascadeConfig(baseUrl, unmanagedValues) {
  const _data = unmanagedValues || {};
  const _ws = {};

  const methods = {
    async subscribe(project, environment, defaults) {
      const flags = Array.from(Object.keys(defaults));
      const disallowedFlags = flags.filter(f => _data[f] !== undefined);
      if (disallowedFlags.length) {
        throw Error(`Can't subscribe to ${project}:${environment}. Flag(s) ${disallowedFlags.join(', ')} are already subscribed.`);
      }

      const websocket = new WebSocket(`ws://${baseUrl}/subscriptions/ws`);
      websocket.onerror = (event) => {
        // TODO - When a connection cannot be established, maybe try using a GET request at intervals.
        console.log('onerror', event);
      };
      websocket.onclose = (event) => {
        // TODO - When a connection is closed, try to reconnect in incremental back-off mode.
        console.log('onclose', event);
      };
      websocket.onmessage = (event) => {
        console.log('onmessage', event);
        const changeset = JSON.parse(event.data);
        const { data } = changeset;
        for (let flagName of Object.keys(data)) {
          // TODO - validate datatype
          _data[flagName] = data[flagName].value;
        }
        // TODO - cache the network values to localstorage
        window.dispatchEvent(new CustomEvent('cascade:updated', {detail: changeset}));
      };
      websocket.onopen = (event) => {
        console.log('onopen', event);
        event.target.send(JSON.stringify({ project, environment, flags }));
//        window.dispatchEvent(new CustomEvent('cascade:connected', {detail: data}));
      };
    }
  };

  return new Proxy(_data, {
    get: function(target, prop, receiver) {
      if (prop in methods) {
        return methods[prop];
      }
      return Reflect.get(...arguments);
    },
    set: function (target, prop, value) {
      throw Error('Config values are read-only');
    },
    deleteProperty: function (target, prop) {
      throw Error('Config values are read-only');
    }
  });
}
