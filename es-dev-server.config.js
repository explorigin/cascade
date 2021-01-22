const proxy = require('koa-proxies');

module.exports = {
  port: 9000,
  debug: true,
  watch: true,
  nodeResolve: true,
  plugins: [],
  moduleDirs: ['node_modules'],
  middlewares: [
    proxy('/api/v1', {
      target: 'http://localhost:9001',
      rewrite: path => path.replace(/^\/api\/v1\/(.*)$/, '/$1'),
      logs:true
    }),
  ],
};
