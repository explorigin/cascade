export function CascadeConfig(baseUrl, defaultValues = {}) {
  const _defaults = defaultValues;
  const _data = {};
  const _types = {}
  const _ws = {};


  function hash(project, environment, flags) {
    return `${project}_${environment}_${flags.sort().join('.')}`
  }

  const dateConverter = (v, o) => {
    const n = new Date(v);
    if (n.toString() === 'Invalid Date') {
      console.error(`Received invalid date value "${value}"`);
      return o;
    }
    return n;
  }
  const compatibleTypeConverter = type => (value, oldValue) => {
    if (typeof value === type) {
      return value;
    }
    console.error(`Received invalid ${type} value "${value}".`);
    return oldValue
  }

  function getConverter(type) {
    switch(type) {
      case 'datetime':
        return dateConverter;
      case 'bool':
        return compatibleTypeConverter('boolean');
      case 'str':
        return compatibleTypeConverter('string');
      case 'int':
        return compatibleTypeConverter('number');
      default:
        console.error(`Received invalid type "${type}"`);
        // Never return the new value
        return (n, o) => o;
    }
  }

  async function subscribe(project, environment, defaults) {
    const flags = Array.from(Object.keys(defaults));
    const disallowedFlags = flags.filter(f => _data[f] !== undefined);
    if (disallowedFlags.length) {
      throw Error(`Can't subscribe to ${project}:${environment}. Flag(s) ${disallowedFlags.join(', ')} are already subscribed.`);
    }

    const subHash = hash(project, environment, flags);
    if (_ws[subHash] !== undefined) {  // Specific check for undefined vs null.
      throw Error(`Already watching ${project}:${environment}. Flag(s) ${flags.join(', ')}.`);
    }

    _ws[subHash] = null;
    const websocket = new WebSocket(`ws://${baseUrl}/subscriptions/ws`);
    websocket.onerror = (e) => {
      // TODO - When a connection cannot be established, maybe try using a GET request at intervals.
      // TODO - Look at localStorage for saved values.
      window.dispatchEvent(new CustomEvent('cascade:error', {detail: {status: e.status}}));
    };
    websocket.onclose = (e) => {
      // TODO - When a connection is closed, try to reconnect in incremental back-off mode.
      window.dispatchEvent(new CustomEvent('cascade:closed'));
    };
    websocket.onmessage = (e) => {
      const changeset = JSON.parse(e.data);
      const { data } = changeset;
      // TODO - validate defaults datatype if the first time. Log an error to the console.
      //  (Values from server are validated on input.)
      for (let flagName of Object.keys(data)) {
        const { datatype, value } = data[flagName];
        if (datatype && !_types[flagName]) {
          _types[flagName] = getConverter(datatype);
          // Validate the default value just so the developer knows they have an invalid default.
          _types[flagName](_defaults[flagName])
          // console.error(`Default value for "${flagName}" does not match authoritative value ${datatype}`);
        }
        _data[flagName] = _types[flagName](value, _data[flagName]);
      }
      // TODO - cache the network values to localstorage
      if (_ws[subHash] === null) {
        _ws[subHash] = e.target;
      }
      window.dispatchEvent(new CustomEvent('cascade:updated', {detail: changeset}));
    };
    websocket.onopen = (e) => {
      e.target.send(JSON.stringify({ project, environment, flags }));
      window.dispatchEvent(new CustomEvent('cascade:connected', {detail: e.target}));
    };
  }

  // TODO - Can't use Proxy in IE11. Switch to Object.defineProperties.
  return new Proxy(_defaults, {
    get: function(target, prop, receiver) {
      if (prop === 'subscribe') {
        return subscribe;
      }
      if (prop in _data) {
        return _data[prop];
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
