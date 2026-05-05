(function () {
  const esc = (s) => String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#39;');

  async function fetchJSON(url) {
    const r = await fetch(url);
    if (!r.ok) throw new Error(`${url} → ${r.status}`);
    return r.json();
  }

  function applySite(site) {
    window.__siteData = site;
    document.querySelectorAll('[data-bind]').forEach(el => {
      const key = el.getAttribute('data-bind');
      const attr = el.getAttribute('data-bind-attr');
      const value = site[key];
      if (value == null) return;
      if (attr) {
        el.setAttribute(attr, value);
        el.textContent = value;
      } else {
        el.textContent = value;
      }
    });
    document.querySelectorAll('[data-bind-html]').forEach(el => {
      const key = el.getAttribute('data-bind-html');
      const value = site[key];
      if (value == null) return;
      el.innerHTML = value;
    });
  }

  function renderStats(stats) {
    const host = document.getElementById('statsList');
    if (!host) return;
    host.innerHTML = stats.map(s => {
      const colorStyle = s.color === 'lime'
        ? ' style="color:var(--lime); text-shadow: var(--glow-lime)"'
        : (s.color === 'purple' ? ' style="color:var(--purple)"' : '');
      return `<div class="stat"><span class="num"${colorStyle}>${esc(s.num)}</span><span class="lbl">${esc(s.label)}</span></div>`;
    }).join('');
  }

  function renderSkills(clusters) {
    const host = document.getElementById('skillsGrid');
    if (!host) return;
    host.innerHTML = clusters.map(c => `
      <article class="skill-card reveal ${esc(c.accent || '')}">
        <div class="skill-head">
          <span class="skill-icon"><i data-lucide="${esc(c.icon || 'code-2')}" aria-hidden="true"></i></span>
          <div>
            <p class="kicker">${esc(c.kicker || '')}</p>
            <h3>${esc(c.title)}</h3>
          </div>
        </div>
        <div class="tags">
          ${(c.tags || []).map(t => `<span class="tag">${esc(t.name)}</span>`).join('')}
        </div>
      </article>
    `).join('');
  }

  function renderProjects(projects) {
    const host = document.getElementById('projectsGrid');
    if (!host) return;
    host.innerHTML = projects.map(p => {
      const links = [];
      if (p.code_url) links.push(`<a class="pc-link" href="${esc(p.code_url)}" target="_blank" rel="noopener"><i data-lucide="github" aria-hidden="true"></i> Code</a>`);
      if (p.live_url) links.push(`<a class="pc-link" href="${esc(p.live_url)}" target="_blank" rel="noopener"><i data-lucide="external-link" aria-hidden="true"></i> Live</a>`);
      return `
        <article class="project-card reveal">
          <div class="pc-head">
            <div>
              <div class="pc-num">${esc(p.num || '')}</div>
              <h3>${esc(p.title)}</h3>
            </div>
            <i class="pc-icon" data-lucide="arrow-up-right" aria-hidden="true"></i>
          </div>
          <div class="tags">
            ${(p.tags || []).map(t => `<span class="tag">${esc(t.name)}</span>`).join('')}
          </div>
          <p class="pc-desc">${esc(p.description || '')}</p>
          <div class="pc-links">${links.join('')}</div>
        </article>
      `;
    }).join('');
  }

  function renderExperience(items) {
    const host = document.getElementById('timeline');
    if (!host) return;
    host.innerHTML = items.map(e => `
      <div class="timeline-item reveal">
        <span class="period">${esc(e.period || '')}</span>
        <h3>${esc(e.role || '')}${e.company ? ` · <span style="color:var(--cyan)">${esc(e.company)}</span>` : ''}</h3>
        <div class="company">${esc(e.company_meta || '')}</div>
        <ul>
          ${(e.bullets || []).map(b => `<li>${esc(b.text)}</li>`).join('')}
        </ul>
      </div>
    `).join('');
  }

  function renderContacts(contacts) {
    const host = document.getElementById('contactList');
    if (!host) return;
    host.innerHTML = contacts.map(c => `
      <a class="contact-row" href="${esc(c.url || '#')}"${/^https?:/i.test(c.url || '') ? ' target="_blank" rel="noopener"' : ''}>
        <span class="ic"><i data-lucide="${esc(c.icon || 'mail')}" aria-hidden="true"></i></span>
        <div>
          <div class="lbl">${esc(c.label || '')}</div>
          <div class="val">${esc(c.value || '')}</div>
        </div>
      </a>
    `).join('');
    const email = contacts.find(c => c.kind === 'email');
    if (email) window.__contactEmail = email.value;
  }

  function postRender() {
    if (window.lucide && window.lucide.createIcons) window.lucide.createIcons();
    if (window.__revealObserver) {
      document.querySelectorAll('.reveal:not(.in)').forEach(el => window.__revealObserver.observe(el));
    } else {
      document.querySelectorAll('.reveal').forEach(el => el.classList.add('in'));
    }
    if (window.__attachTilt) {
      document.querySelectorAll('.project-card').forEach(c => {
        if (c.__tiltAttached) return;
        c.__tiltAttached = true;
        window.__attachTilt(c);
      });
    }
    if (window.__applyLang) window.__applyLang();
  }

  async function init() {
    try {
      const [site, stats, contacts, clusters, projects, experience] = await Promise.all([
        fetchJSON('/api/site'),
        fetchJSON('/api/stats'),
        fetchJSON('/api/contacts'),
        fetchJSON('/api/skill-clusters'),
        fetchJSON('/api/projects'),
        fetchJSON('/api/experience'),
      ]);
      applySite(site);
      renderStats(stats);
      renderSkills(clusters);
      renderProjects(projects);
      renderExperience(experience);
      renderContacts(contacts);
      postRender();
    } catch (err) {
      console.error('site.js: failed to load data', err);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
