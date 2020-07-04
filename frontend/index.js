import { CascadeConfig } from "./CascadeConfig";
import { SubscriptionForm } from './components/SubscriptionForm';
import { DisplayConfig } from './components/DisplayConfig';
import { DemoApp } from './DemoApp';

window.config = CascadeConfig(
  `${window.location.host}:8000`,
  {
    debug: true,
    idp_mgmt_username: '',
    log_to_console: false
  }
);

window.addEventListener('cascade:updated', console.log.bind(console));
window.addEventListener('cascade:connected', console.log.bind(console));
