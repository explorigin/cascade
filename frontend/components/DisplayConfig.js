import {LitElement, html, css} from '/node_modules/lit-element/lit-element.js';

export class DisplayConfig extends LitElement {
  static get styles() {
    return css`
      :host {
        flex: 1;
      }
    `;
  }

  static get properties() {
    return {
      config: {type: Object}
    }
  }

  constructor(config) {
    super();
    const update = evt => {
      this.config = evt.detail;
    };
    window.addEventListener('cascade:updated', update);
    window.addEventListener('cascade:connected', update);
    this.config = window.config;
  }

  render() {
    return html`
      <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/5.0.0-alpha1/css/bootstrap.min.css" integrity="sha384-r4NyP46KrjDleawBgD5tp8Y7UzmLA05oM1iAEQ17CSuDqnUK2+k9luXQOfXJCJ4I" crossorigin="anonymous">
 
      <div class="container">
        <dl>
        ${Object.entries(window.config).map(([key, value]) => {
          return html`<dt>${key}</dt><dd>${value}</dd>`    
        })}
        </dl>
      </div>
    `;
  }
}

customElements.define('display-config', DisplayConfig);
