import { CascadeConfig } from "./CascadeConfig";
import { SubscriptionForm } from './components/SubscriptionForm';
import { DisplayConfig } from './components/DisplayConfig';
import { DemoApp } from './DemoApp';

window.config = CascadeConfig(
  `${window.location.hostname}:8001`,
  {
    debug: 'dued',
    astra_endpoint: 'http://example.com',
    idp_mgmt_username: 'bob'
  }
);

window.addEventListener('cascade:updated', console.log.bind(console));
window.addEventListener('cascade:connected', console.log.bind(console));
