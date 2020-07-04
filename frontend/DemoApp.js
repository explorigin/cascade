import {LitElement, html, css} from '/node_modules/lit-element/lit-element.js';

export class DemoApp extends LitElement {
  static get styles() {
    return css`
      :host {
        flex: 1;
        display: flex;
        flex-direction: row;
      }
    `;
  }

  constructor() {
    super();
  }

  render() {
    return html`
      <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/5.0.0-alpha1/css/bootstrap.min.css" integrity="sha384-r4NyP46KrjDleawBgD5tp8Y7UzmLA05oM1iAEQ17CSuDqnUK2+k9luXQOfXJCJ4I" crossorigin="anonymous">
      
      <subscription-form></subscription-form>
      <display-config></display-config>
    `;
  }
}

customElements.define('demo-app', DemoApp);
