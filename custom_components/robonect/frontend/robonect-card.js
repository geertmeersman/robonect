const ROBONECT_I18N = {
  nl: {
    duration: 'Duur', blades: 'Messen', alarm: 'Alarm', distance: 'Afstand',
    battery: 'Batterij', wifi: 'WiFi', temp: 'Temp', humidity: 'Vocht',
    current: 'Stroom', voltage: 'Spanning', capacity: 'Capaciteit',
    winter: 'Winter', stopped: 'Gestopt — klik om te starten',
    next_start: 'Volgende start',
    at: 'om',
    weather_stop: 'Gestopt omwille van het weer',
    winter_active: 'Wintermode actief',
    days: ['zo','ma','di','wo','do','vr','za'],
    months: ['jan','feb','mrt','apr','mei','jun','jul','aug','sep','okt','nov','dec'],
  },
  en: {
    duration: 'Duration', blades: 'Blades', alarm: 'Alarm', distance: 'Distance',
    battery: 'Battery', wifi: 'WiFi', temp: 'Temp', humidity: 'Humidity',
    current: 'Current', voltage: 'Voltage', capacity: 'Capacity',
    winter: 'Winter', stopped: 'Stopped — click to start',
    next_start: 'Next start',
    at: 'at',
    weather_stop: 'Stopped due to weather',
    winter_active: 'Winter mode active',
    days: ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'],
    months: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
  },
  de: {
    duration: 'Dauer', blades: 'Messer', alarm: 'Alarm', distance: 'Distanz',
    battery: 'Batterie', wifi: 'WiFi', temp: 'Temp', humidity: 'Feuchte',
    current: 'Strom', voltage: 'Spannung', capacity: 'Kapazität',
    winter: 'Winter', stopped: 'Gestoppt — klicken zum Starten',
    next_start: 'Nächster Start',
    at: 'um',
    weather_stop: 'Gestoppt wegen Wetter',
    winter_active: 'Wintermodus aktiv',
    days: ['So','Mo','Di','Mi','Do','Fr','Sa'],
    months: ['Jan','Feb','Mär','Apr','Mai','Jun','Jul','Aug','Sep','Okt','Nov','Dez'],
  },
  fr: {
    duration: 'Durée', blades: 'Lames', alarm: 'Alarme', distance: 'Distance',
    battery: 'Batterie', wifi: 'WiFi', temp: 'Temp', humidity: 'Humidité',
    current: 'Courant', voltage: 'Tension', capacity: 'Capacité',
    winter: 'Hiver', stopped: 'Arrêté — cliquer pour démarrer',
    next_start: 'Prochain démarrage',
    at: 'à',
    weather_stop: 'Arrêté à cause de la météo',
    winter_active: 'Mode hiver actif',
    days: ['Dim','Lun','Mar','Mer','Jeu','Ven','Sam'],
    months: ['Jan','Fév','Mar','Avr','Mai','Jun','Jul','Aoû','Sep','Oct','Nov','Déc'],
  },
};

class RobonectCard extends HTMLElement {
  set hass(hass) {
    const old = this._hass;
    this._hass = hass;
    if (this._childCards) this._childCards.forEach(c => { c.hass = hass; });
    if (!old) this._render();
    else this._updateDynamic();
  }

  setConfig(config) {
    this._config = config;
    this._childCards = [];
    this._rendered = false;
    this._prefix = null;
  }

  _t(key) {
    const lang = this._hass?.locale?.language?.toLowerCase().split('-')[0] || 'nl';
    return (ROBONECT_I18N[lang] || ROBONECT_I18N.nl)[key] || ROBONECT_I18N.nl[key] || key;
  }

  _detectPrefix() {
    if (this._prefix) return this._prefix;
    if (!this._hass) return 'automower';
    const lawnMower = Object.keys(this._hass.states).find(id => id.startsWith('lawn_mower.'));
    if (lawnMower) this._prefix = lawnMower.replace('lawn_mower.', '').replace('_robonect', '');
    else this._prefix = 'automower';
    return this._prefix;
  }

  _e(suffix) { return `sensor.${this._detectPrefix()}_${suffix}`; }
  _eb(suffix) { return `binary_sensor.${this._detectPrefix()}_${suffix}`; }
  _btn(suffix) { return `button.${this._detectPrefix()}_${suffix}`; }
  _sw(suffix) { return `switch.${this._detectPrefix()}_${suffix}`; }
  _s(id) { return this._hass?.states[id]?.state; }
  _a(id, attr) { return this._hass?.states[id]?.attributes?.[attr]; }
  _fmt(id) {
    const s = this._hass?.states[id];
    if (!s) return '—';
    const val = s.state;
    if (['unknown', 'unavailable'].includes(val)) return '—';
    const unit = s.attributes?.unit_of_measurement || '';
    return `${val}${unit ? ' ' + unit : ''}`;
  }

  _moreInfo(id) {
    this.dispatchEvent(new CustomEvent('hass-more-info', { detail: { entityId: id }, bubbles: true, composed: true }));
  }

  _updateDynamic() {
    if (!this._rendered) return;
    const status = this._s(this._e('mower_status'));
    const winterMode = this._s(this._eb('winter_mode')) === 'on';
    const stopped = this._s(this._eb('mower_stopped')) === 'on';
    const weatherBreak = this._s(this._eb('weather_data_break')) === 'on';
    const mode = this._s(this._e('mower_mode'));

    // Update header name
    const headerName = this.querySelector('#header-name');
    if (headerName) {
      const lawnEntity = Object.keys(this._hass.states).find(id => id.startsWith('lawn_mower.'));
      const friendlyName = this._hass.states[lawnEntity]?.attributes?.friendly_name || 'Grasmaaier';
      const name = this._hass.entities?.[lawnEntity]?.name || friendlyName.replace(/^.*?\s/, '') || friendlyName;
      headerName.textContent = name;
    }

    // Error banner
    const errorBanner = this.querySelector('#error-banner');
    if (errorBanner) {
      errorBanner.style.display = status === '7' ? '' : 'none';
      const errMsg = this.querySelector('#error-msg');
      if (errMsg) errMsg.textContent = this._s(this._e('mower_error_message')) || '';
    }

    // Winter toggle button
    const winterToggle = this.querySelector('#winter-toggle');
    if (winterToggle) winterToggle.classList.toggle('active', winterMode);

    // Winter / normal
    const winterSection = this.querySelector('#winter-section');
    const normalSection = this.querySelector('#normal-section');
    if (winterSection) winterSection.style.display = winterMode ? '' : 'none';
    if (normalSection) normalSection.style.display = winterMode ? 'none' : '';

    // Stopped banner
    const stoppedBanner = this.querySelector('#stopped-banner');
    if (stoppedBanner) stoppedBanner.style.display = stopped ? '' : 'none';

    // Weather break
    const weatherBanner = this.querySelector('#weather-banner');
    if (weatherBanner) {
      weatherBanner.style.display = weatherBreak ? '' : 'none';
      if (weatherBreak) {
        const weatherData = { toorainy: 'teveel regen', toocold: 'te koud', toowarm: 'te warm', toodry: 'te droog', toowet: 'te nat', day: 'overdag', night: "'s nachts" };
        const conditions = this._a(this._eb('weather_service'), 'weather')?.condition || {};
        const reasons = Object.entries(conditions).filter(([, v]) => v).map(([k]) => weatherData[k] || k).join(', ');
        const wMsg = this.querySelector('#weather-msg');
        if (wMsg) wMsg.textContent = `${this._t('weather_stop')}: ${reasons}`;
      }
    }

    // Timer
    const timerSection = this.querySelector('#timer-section');
    const timerMsg = this.querySelector('#timer-msg');
    const nextTimer = this._s(this._e('mower_timer_next_unix'));
    if (timerSection && nextTimer && !['unknown', 'unavailable'].includes(nextTimer)) {
      timerSection.style.display = '';
      const d = new Date(nextTimer);
      const days = this._t('days');
      const months = this._t('months');
      const at = this._t('at');
      if (timerMsg) timerMsg.textContent = `${this._t('next_start')}: ${days[d.getDay()]} ${d.getDate()} ${months[d.getMonth()]} ${at} ${d.getHours().toString().padStart(2,'0')}:${d.getMinutes().toString().padStart(2,'0')}`;
    } else if (timerSection) {
      timerSection.style.display = 'none';
    }

    // Mode buttons
    ['0', '1', '2'].forEach((m, i) => {
      const btn = this.querySelector(`#mode-btn-${i}`);
      if (btn) {
        btn.style.background = mode === m ? 'var(--state-active-color)' : 'var(--secondary-background-color)';
        btn.style.color = mode === m ? 'white' : 'var(--primary-text-color)';
      }
    });

    // Stats tiles
    const stats = [
      { id: 'stat-duration', entity: this._e('mower_status_duration'), label: 'Duur', icon: 'mdi:timer' },
      { id: 'stat-blades', entity: this._e('mower_blades_quality'), label: 'Messen', icon: 'mdi:fan' },
      { id: 'stat-alarm', entity: this._eb('health_alarm'), label: 'Alarm', icon: 'mdi:alarm-light' },
      { id: 'stat-distance', entity: this._e('mower_distance'), label: 'Afstand', icon: 'mdi:map-marker-distance' },
      { id: 'stat-battery', entity: this._e('mower_battery_charge'), label: 'Batterij', icon: 'mdi:battery' },
      { id: 'stat-rssi', entity: this._e('wlan_rssi'), label: 'WiFi', icon: 'mdi:wifi' },
      { id: 'stat-temp', entity: this._e('health_climate_temperature'), label: 'Temp', icon: 'mdi:thermometer' },
      { id: 'stat-humidity', entity: this._e('health_climate_humidity'), label: 'Vocht', icon: 'mdi:water-percent' },
    ];
    stats.forEach(({ id, entity }) => {
      const el = this.querySelector(`#${id} .stat-value`);
      if (el) el.textContent = this._fmt(entity);
    });

    // Gauges
    const batteryGauges = [
      { id: 'gauge-current', attr: 'current', unit: 'mA', min: -1500, max: 1500 },
      { id: 'gauge-voltage', attr: 'voltage', unit: 'V', min: 0, max: 30 },
      { id: 'gauge-capacity', attr: 'capacity', unit: 'mAh', min: 0, max: 1600 },
      { id: 'gauge-temp', attr: 'temperature', unit: '°C', min: -10, max: 50 },
    ];
    batteryGauges.forEach(({ id, attr, unit, min, max }) => {
      const el = this.querySelector(`#${id}`);
      if (!el) return;
      let val;
      if (attr === 'capacity') {
        const cap = this._a(this._e('battery_0'), 'capacity');
        val = cap ? parseFloat(String(cap.remaining).replace(/[^0-9.-]/g, '')) : null;
      } else {
        const raw = this._a(this._e('battery_0'), attr);
        val = raw !== null && raw !== undefined ? parseFloat(String(raw).replace(/[^0-9.-]/g, '')) : null;
      }
      el.querySelector('.gauge-value').textContent = val !== null && !isNaN(val) ? `${val} ${unit}` : '—';
      const indicator = el.querySelector('.gauge-indicator');
      if (indicator && val !== null && !isNaN(val)) {
        const pct = Math.max(0, Math.min(100, ((val - min) / (max - min)) * 100));
        indicator.style.left = `${pct}%`;
      }
    });
  }

  async _render() {
    if (!this._hass) return;
    this._rendered = true;

    const statTile = (id, entity, label, icon) => `
      <div class="stat-tile" id="${id}" data-entity="${entity}">
        <div class="stat-label"><ha-icon icon="${icon}"></ha-icon>${label}</div>
        <div class="stat-value">—</div>
      </div>`;

    const gaugeItem = (id, entity, label, segments) => {
      const segStr = segments.map(s => `<div class="gauge-seg" style="background:${s.color};flex:${s.flex}"></div>`).join('');
      return `
      <div class="gauge-item" id="${id}" data-entity="${entity}">
        <div class="gauge-label">${label}</div>
        <div class="gauge-bar">${segStr}<div class="gauge-indicator"></div></div>
        <div class="gauge-value">—</div>
      </div>`;
    };

    this.innerHTML = `
      <ha-card>
        <style>
          ha-card { overflow: hidden; border-radius: var(--ha-card-border-radius, 12px); }
          .banner { padding: 8px 12px; display: flex; align-items: center; gap: 8px; font-size: 0.85em; font-weight: 600; cursor: pointer; }
          .banner ha-icon { --mdc-icon-size: 18px; flex-shrink: 0; }
          .banner.error { background: var(--error-color); color: white; }
          .banner.warning { background: var(--warning-color); color: white; }
          .banner.info { background: var(--info-color, #2196f3); color: white; }
          .timer-section { padding: 6px 12px; text-align: center; font-size: 0.8em; color: var(--secondary-text-color); border-bottom: 1px solid var(--divider-color); }
          .stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1px; background: var(--divider-color); border-top: 1px solid var(--divider-color); border-bottom: 1px solid var(--divider-color); }
          .stat-tile { background: var(--card-background-color); padding: 10px 8px; cursor: pointer; display: flex; flex-direction: column; gap: 4px; }
          .stat-tile:hover { filter: brightness(1.05); }
          .stat-label { font-size: 0.68em; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: var(--secondary-text-color); display: flex; align-items: center; gap: 3px; }
          .stat-label ha-icon { --mdc-icon-size: 12px; }
          .stat-value { font-size: 1em; font-weight: 700; }
          .lawn-mower-section { padding: 8px 12px; }
          .mode-btns { display: flex; gap: 6px; padding: 0 12px 10px; }
          .mode-btn { flex: 1; height: 44px; border: none; border-radius: 8px; background: var(--secondary-background-color); color: var(--primary-text-color); cursor: pointer; display: flex; align-items: center; justify-content: center; transition: background 0.2s; }
          .mode-btn:hover { filter: brightness(1.1); }
          .mode-btn ha-icon { --mdc-icon-size: 22px; }
          .gauges { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1px; background: var(--divider-color); border-top: 1px solid var(--divider-color); }
          .gauge-item { background: var(--card-background-color); display: flex; flex-direction: column; align-items: center; gap: 4px; padding: 10px 8px; cursor: pointer; }
          .gauge-item:hover { filter: brightness(1.05); }
          .gauge-label { font-size: 0.68em; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: var(--secondary-text-color); }
          .gauge-bar { display: flex; width: 100%; height: 6px; border-radius: 3px; overflow: visible; position: relative; }
          .gauge-seg { height: 100%; }
          .gauge-indicator { position: absolute; top: -4px; width: 4px; height: 14px; background: var(--primary-text-color); border-radius: 2px; transform: translateX(-50%); pointer-events: none; left: 0%; }
          .gauge-value { font-size: 0.85em; font-weight: 700; }
          .header { display: flex; align-items: center; gap: 10px; padding: 12px 14px; border-bottom: 1px solid var(--divider-color); }
          .header img { height: 36px; width: 36px; border-radius: 50%; background: var(--secondary-background-color); padding: 4px; object-fit: contain; }
          .header-name { font-size: 1em; font-weight: 700; flex: 1; }
          .winter-toggle { border: none; border-radius: 6px; padding: 4px 8px; cursor: pointer; display: flex; align-items: center; gap: 4px; font-size: 0.75em; font-weight: 600; background: var(--secondary-background-color); color: var(--secondary-text-color); }
          .winter-toggle.active { background: var(--info-color, #2196f3); color: white; }
          .winter-toggle ha-icon { --mdc-icon-size: 14px; pointer-events: none; }
          .winter-section ha-icon { --mdc-icon-size: 48px; color: var(--info-color, #2196f3); }
          .winter-section span { font-weight: 600; font-size: 1em; }
        </style>

        <div class="banner error" id="error-banner" style="display:none;">
          <ha-icon icon="mdi:alert"></ha-icon><span id="error-msg"></span>
        </div>

        <div class="header">
          <img src="/robonect/robonect-icon.png" alt="Robonect" onerror="this.style.display='none'">
          <span class="header-name" id="header-name">Grasmaaier</span>
          <button class="winter-toggle" id="winter-toggle"><ha-icon icon="mdi:snowflake"></ha-icon>${this._t('winter')}</button>
        </div>

        <div id="winter-section" class="winter-section" style="display:none;">
          <ha-icon icon="mdi:snowflake"></ha-icon>
          <span>${this._t('winter_active')}</span>
        </div>

        <div id="normal-section">
          <div class="timer-section" id="timer-section" style="display:none;">
            <span id="timer-msg"></span>
          </div>

          <div class="banner warning" id="stopped-banner" style="display:none;">
            <ha-icon icon="mdi:pause-circle"></ha-icon>
            <span>${this._t('stopped')}</span>
          </div>

          <div class="banner info" id="weather-banner" style="display:none;">
            <ha-icon icon="mdi:weather-rainy"></ha-icon>
            <span id="weather-msg"></span>
          </div>

          <div class="stats-grid">
            ${statTile('stat-duration', this._e('mower_status_duration'), this._t('duration'), 'mdi:timer')}
            ${statTile('stat-blades', this._e('mower_blades_quality'), this._t('blades'), 'mdi:fan')}
            ${statTile('stat-alarm', this._eb('health_alarm'), this._t('alarm'), 'mdi:alarm-light')}
            ${statTile('stat-distance', this._e('mower_distance'), this._t('distance'), 'mdi:map-marker-distance')}
            ${statTile('stat-battery', this._e('mower_battery_charge'), this._t('battery'), 'mdi:battery')}
            ${statTile('stat-rssi', this._e('wlan_rssi'), this._t('wifi'), 'mdi:wifi')}
            ${statTile('stat-temp', this._e('health_climate_temperature'), this._t('temp'), 'mdi:thermometer')}
            ${statTile('stat-humidity', this._e('health_climate_humidity'), this._t('humidity'), 'mdi:water-percent')}
          </div>

          <div class="lawn-mower-section" id="lawn-mower-slot"></div>

          <div class="mode-btns">
            <button class="mode-btn" id="mode-btn-0"><ha-icon icon="mdi:calendar-clock"></ha-icon></button>
            <button class="mode-btn" id="mode-btn-1"><ha-icon icon="mdi:hand-wave"></ha-icon></button>
            <button class="mode-btn" id="mode-btn-2"><ha-icon icon="mdi:weather-sunset-down"></ha-icon></button>
          </div>

          <div class="gauges">
            ${gaugeItem('gauge-current', this._e('battery_0'), this._t('current'), [{color:'var(--info-color)',flex:1},{color:'var(--success-color)',flex:1}])}
            ${gaugeItem('gauge-voltage', this._e('battery_0'), this._t('voltage'), [{color:'var(--error-color)',flex:2},{color:'var(--warning-color)',flex:1},{color:'var(--success-color)',flex:2}])}
            ${gaugeItem('gauge-capacity', this._e('battery_0'), this._t('capacity'), [{color:'var(--error-color)',flex:1},{color:'var(--warning-color)',flex:2},{color:'var(--success-color)',flex:3}])}
            ${gaugeItem('gauge-temp', this._e('battery_0'), this._t('temp'), [{color:'var(--error-color)',flex:1},{color:'var(--warning-color)',flex:1},{color:'var(--success-color)',flex:2},{color:'var(--warning-color)',flex:1}])}
          </div>
        </div>
      </ha-card>`;

    // Lawn mower tile
    const lawnSlot = this.querySelector('#lawn-mower-slot');
    try {
      const helpers = await window.loadCardHelpers();
      const lawnEntity = Object.keys(this._hass.states).find(id => id.startsWith('lawn_mower.'));
      const lawnCard = await helpers.createCardElement({
        type: 'tile',
        entity: lawnEntity,
        show_entity_picture: true,
        vertical: true,
        name: { type: 'entity' },
        features: [{ type: 'lawn-mower-commands', commands: ['start_pause', 'dock'] }],
      });
      lawnCard.hass = this._hass;
      lawnSlot.appendChild(lawnCard);
      this._childCards.push(lawnCard);
    } catch (e) {}

    // Click handlers
    this.querySelectorAll('.stat-tile[data-entity]').forEach(el => {
      el.addEventListener('click', () => this._moreInfo(el.dataset.entity));
    });
    this.querySelectorAll('.gauge-item[data-entity]').forEach(el => {
      el.addEventListener('click', () => this._moreInfo(el.dataset.entity));
    });

    const winterToggleBtn = this.querySelector('#winter-toggle');
    if (winterToggleBtn) {
      winterToggleBtn.addEventListener('click', () => this._moreInfo(this._sw('winter_mode')));
    }

    const stoppedBanner = this.querySelector('#stopped-banner');
    if (stoppedBanner) {
      stoppedBanner.addEventListener('click', () => {
        this._hass.callService('button', 'press', { entity_id: this._btn('start') });
      });
    }

    [['mode-btn-0', this._btn('auto')], ['mode-btn-1', this._btn('man')], ['mode-btn-2', this._btn('eod')]].forEach(([id, entity]) => {
      const btn = this.querySelector(`#${id}`);
      if (btn) btn.addEventListener('click', () => this._hass.callService('button', 'press', { entity_id: entity }));
    });

    this._updateDynamic();
  }

  getCardSize() { return 5; }
  static getStubConfig() { return {}; }
}

customElements.define('robonect-card', RobonectCard);

window.customCards = window.customCards || [];
if (!window.customCards.find(c => c.type === 'robonect-card')) {
  window.customCards.push({ type: 'robonect-card', name: 'Robonect Card', description: 'Card for Robonect lawn mower.', supportedTypes: ['lawn_mower'],
    getEntitySuggestion: (hass, entityId) => entityId.startsWith('lawn_mower.') ? [{ label: 'Robonect Card', config: { type: 'custom:robonect-card' } }] : null });
}
