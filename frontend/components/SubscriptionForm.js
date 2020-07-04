import {LitElement, html, css} from '/node_modules/lit-element/lit-element.js';

export class SubscriptionForm extends LitElement {
  static get properties() {
    return {
      project: {type: String},
      environment: {type: String},
    };
  }

  static get styles() {
    return css`
      :host {
        flex: 1;
      }
    `;
  }

  constructor() {
    super();
    this.project = '';
    this.environment = '';
  }

  async subscribe(evt) {
    evt.preventDefault();
    const data = new FormData(evt.target);
    const project = data.get('project');
    const environment = data.get('environment');
    const flags = data.getAll('flags').filter(f => !!f);
    const flagData = flags.reduce((a, f) => { a[f] = ''; return a; }, {});
    await window.config.subscribe(project, environment, flagData);
    let event = new CustomEvent('subscribed', window.config);
    this.dispatchEvent(event);
  }

  render() {
    return html`
      <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/5.0.0-alpha1/css/bootstrap.min.css" integrity="sha384-r4NyP46KrjDleawBgD5tp8Y7UzmLA05oM1iAEQ17CSuDqnUK2+k9luXQOfXJCJ4I" crossorigin="anonymous">
      
      <div class="container">
        <form @submit="${this.subscribe}">
          <div class="row mb-3">
            <label for="project" class="col-sm-2 col-form-label">Project</label>
            <div class="col-sm-10">
              <input type="text" class="form-control" name="project" autofocus .value="${this.project}">
            </div>
          </div>
          <div class="row mb-3">
            <label for="environment" class="col-sm-2 col-form-label">Environment</label>
            <div class="col-sm-10">
              <input type="text" class="form-control" name="environment" .value="${this.environment}">
            </div>
          </div>
          <fieldset>
            <div class="row mb-3">
              <legend class="col-form-label col-sm-2 pt-0">Flags</legend>
              <div class="col-sm-10">
                <div class="form-check">
                  <input type="text" class="form-control" name="flags">
                </div>
                <div class="form-check">
                    <input type="text" class="form-control" name="flags">
                </div>
                <div class="form-check">
                    <input type="text" class="form-control" name="flags">
                </div>
              </div>
            </div>
          </fieldset>
          <button type="submit" class="btn btn-primary">Subscribe</button>
        </form>
      </div>
    `;
  }
}

customElements.define('subscription-form', SubscriptionForm);
