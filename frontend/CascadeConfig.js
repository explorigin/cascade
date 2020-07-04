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
      const res = await fetch(
        `//${baseUrl}/subscriptions/${project}/${environment}`,
        {
          method: 'POST',
          body: JSON.stringify(flags)
        }
      );
      if (res.status !== 201) {
        throw Error(`Failed to subscribe: ${await res.text()}`);
      }
      // TODO - if the network call fails, use the defaults, but check localstorage
      const {key, data} = await res.json();
      for (let flagName of Object.keys(data)) {
        // TODO - validate datatype
        _data[flagName] = data[flagName].value;
      }
      // TODO - cache the network values to localstorage

      _ws[key] = new WebSocket(`ws://${baseUrl}/subscriptions/${key}/ws`);
      _ws[key].onerror = (event) => {
        // TODO - When a connection cannot be established, maybe try using a GET request at intervals.
      };
      _ws[key].onclose = (event) => {
        // TODO - When a connection is closed, try to reconnect in incremental back-off mode.
      };
      _ws[key].onmessage = (event) => {
        const changeset = JSON.parse(event.data);
        const {project, environment, data} = changeset;
        for (let flagName of Object.keys(data)) {
          // TODO - validate datatype
          _data[flagName] = data[flagName].value;
        }
        // TODO - cache the network values to localstorage
        window.dispatchEvent(new CustomEvent('cascade:updated', {detail: changeset}));
      };
      window.dispatchEvent(new CustomEvent('cascade:connected', {detail: data}));
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
