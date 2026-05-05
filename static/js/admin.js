(function () {
  const TOKEN_KEY = 'admin_token';
  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));
  const esc = (s) => String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#39;');

  function token() { return localStorage.getItem(TOKEN_KEY); }
  function setToken(t) { if (t) localStorage.setItem(TOKEN_KEY, t); else localStorage.removeItem(TOKEN_KEY); }

  async function api(method, path, body) {
    const headers = { 'Content-Type': 'application/json' };
    const t = token();
    if (t) headers['Authorization'] = `Bearer ${t}`;
    const r = await fetch(path, {
      method, headers,
      body: body == null ? undefined : JSON.stringify(body),
    });
    if (r.status === 401 || r.status === 403) {
      setToken(null);
      showLogin();
      throw new Error('unauthorized');
    }
    if (!r.ok) {
      const text = await r.text().catch(() => '');
      throw new Error(`${method} ${path} → ${r.status} ${text}`);
    }
    if (r.status === 204) return null;
    return r.json();
  }

  function toast(msg, isError) {
    const t = $('#toast');
    t.textContent = msg;
    t.classList.toggle('error', !!isError);
    t.classList.add('show');
    clearTimeout(toast._h);
    toast._h = setTimeout(() => t.classList.remove('show'), 2200);
  }

  // ---------- auth screens ----------

  function showLogin() {
    $('#dashboard').hidden = true;
    $('#loginScreen').hidden = false;
    $('#adminPwd').focus();
  }
  function showDashboard() {
    $('#loginScreen').hidden = true;
    $('#dashboard').hidden = false;
    selectSection('site');
  }

  $('#loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    $('#loginError').textContent = '';
    const password = $('#adminPwd').value;
    try {
      const r = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password }),
      });
      if (!r.ok) {
        $('#loginError').textContent = '[error] wrong password';
        return;
      }
      const { token: tok } = await r.json();
      setToken(tok);
      $('#adminPwd').value = '';
      showDashboard();
    } catch (err) {
      $('#loginError').textContent = '[error] ' + err.message;
    }
  });

  $('#logoutBtn').addEventListener('click', () => {
    setToken(null);
    showLogin();
  });

  $$('.sidebar button[data-section]').forEach(btn => {
    btn.addEventListener('click', () => selectSection(btn.dataset.section));
  });

  function selectSection(name) {
    $$('.sidebar button[data-section]').forEach(b =>
      b.classList.toggle('active', b.dataset.section === name)
    );
    const fn = SECTIONS[name];
    if (fn) fn();
  }

  // ---------- section: site settings ----------

  const SITE_GROUPS = [
    { title: 'Hero', keys: [
      ['hero_badge', 'input', 'Badge text'],
      ['hero_title_prefix', 'input', 'Title prefix'],
      ['hero_name', 'input', 'Name'],
      ['hero_desc_en', 'textarea', 'Description (EN)'],
      ['hero_desc_ru', 'textarea', 'Description (RU)'],
      ['hero_meta_location', 'input', 'Meta · location'],
      ['hero_meta_exp', 'input', 'Meta · experience'],
      ['hero_meta_stack', 'input', 'Meta · stack'],
    ]},
    { title: 'About', keys: [
      ['about_title_html', 'textarea', 'About title (HTML allowed)'],
      ['about_p1', 'textarea', 'Paragraph 1 (HTML allowed)'],
      ['about_p2', 'textarea', 'Paragraph 2 (HTML allowed)'],
      ['about_p3', 'textarea', 'Paragraph 3 (HTML allowed)'],
      ['about_p4', 'textarea', 'Paragraph 4 (HTML allowed)'],
    ]},
    { title: 'Section subs', keys: [
      ['section_about_sub', 'textarea', 'About sub'],
      ['section_skills_sub', 'textarea', 'Skills sub'],
      ['section_projects_sub', 'textarea', 'Projects sub'],
      ['section_experience_sub', 'textarea', 'Experience sub'],
      ['section_contact_sub', 'textarea', 'Contact sub'],
    ]},
    { title: 'Footer', keys: [
      ['footer_copy', 'input', 'Footer copyright'],
    ]},
  ];

  async function renderSite() {
    const data = await api('GET', '/api/site');
    const main = $('#main');
    main.innerHTML = `
      <h2>Site settings</h2>
      <p class="lead">Edit the singleton text fields shown across the public page.</p>
      <form id="siteForm">
        ${SITE_GROUPS.map(g => `
          <div class="card">
            <h3>${esc(g.title)}</h3>
            ${g.keys.map(([k, kind, lbl]) => `
              <div class="field">
                <label for="sk-${k}">${esc(lbl)} <span style="color:var(--fg-mute)">[${k}]</span></label>
                ${kind === 'textarea'
                  ? `<textarea id="sk-${k}" name="${k}">${esc(data[k] || '')}</textarea>`
                  : `<input id="sk-${k}" name="${k}" type="text" value="${esc(data[k] || '')}" />`}
              </div>
            `).join('')}
          </div>
        `).join('')}
        <button class="btn btn-primary" type="submit">Save all</button>
      </form>
    `;
    $('#siteForm').addEventListener('submit', async (e) => {
      e.preventDefault();
      const payload = {};
      $$('#siteForm input, #siteForm textarea').forEach(el => { payload[el.name] = el.value; });
      try {
        await api('PATCH', '/api/site', payload);
        toast('saved');
      } catch (err) { toast(err.message, true); }
    });
  }

  // ---------- section: stats ----------

  async function renderStats() {
    const items = await api('GET', '/api/stats');
    const main = $('#main');
    main.innerHTML = `
      <h2>Stats</h2>
      <p class="lead">Rows shown in the "quick.stats" card.</p>
      <div class="card">
        <h3>Existing</h3>
        <div class="row-list">${items.map(s => `
          <div class="row-item" data-id="${s.id}">
            <div class="meta">
              <strong>${esc(s.num)}</strong> · ${esc(s.label)}
              <div class="sub">color: ${esc(s.color || '—')} · order: ${s.order}</div>
            </div>
            <div class="actions">
              <button class="btn btn-sm" data-act="up">↑</button>
              <button class="btn btn-sm" data-act="down">↓</button>
              <button class="btn btn-sm" data-act="edit">edit</button>
              <button class="btn btn-sm btn-danger" data-act="del">del</button>
            </div>
          </div>
        `).join('') || '<div class="meta sub">No stats yet.</div>'}</div>
      </div>
      <div class="card">
        <h3>Add new</h3>
        <form id="statForm" class="grid-3">
          <div class="field"><label>num</label><input name="num" required placeholder="4+" /></div>
          <div class="field"><label>label</label><input name="label" required placeholder="years in IT" /></div>
          <div class="field"><label>color</label>
            <select name="color"><option value="">(default cyan)</option><option value="lime">lime</option><option value="purple">purple</option></select>
          </div>
          <button class="btn btn-primary" type="submit" style="grid-column: 1 / -1; justify-self: start">Add stat</button>
        </form>
      </div>
    `;
    bindRowActions(items, 'stats', renderStats, ['num', 'label', 'color']);
    $('#statForm').addEventListener('submit', async (e) => {
      e.preventDefault();
      const f = e.target;
      const body = {
        num: f.num.value, label: f.label.value, color: f.color.value,
        order: items.length,
      };
      try { await api('POST', '/api/stats', body); toast('added'); renderStats(); }
      catch (err) { toast(err.message, true); }
    });
  }

  // ---------- section: contacts ----------

  async function renderContacts() {
    const items = await api('GET', '/api/contacts');
    const main = $('#main');
    main.innerHTML = `
      <h2>Contacts</h2>
      <p class="lead">Rows shown in the contact list (email, github, linkedin, telegram, …).</p>
      <div class="card">
        <h3>Existing</h3>
        <div class="row-list">${items.map(c => `
          <div class="row-item" data-id="${c.id}">
            <div class="meta">
              [${esc(c.kind)}] <strong>${esc(c.label)}</strong> · ${esc(c.value)}
              <div class="sub">url: ${esc(c.url || '—')} · icon: ${esc(c.icon)} · order: ${c.order}</div>
            </div>
            <div class="actions">
              <button class="btn btn-sm" data-act="up">↑</button>
              <button class="btn btn-sm" data-act="down">↓</button>
              <button class="btn btn-sm" data-act="edit">edit</button>
              <button class="btn btn-sm btn-danger" data-act="del">del</button>
            </div>
          </div>`).join('') || '<div class="meta sub">No contacts yet.</div>'}</div>
      </div>
      <div class="card">
        <h3>Add new</h3>
        <form id="contactForm" class="grid-3">
          <div class="field"><label>kind</label><input name="kind" required placeholder="email" /></div>
          <div class="field"><label>label</label><input name="label" required placeholder="email" /></div>
          <div class="field"><label>icon (lucide name)</label><input name="icon" required placeholder="mail" /></div>
          <div class="field"><label>value</label><input name="value" required placeholder="hello@..." /></div>
          <div class="field" style="grid-column: span 2"><label>url</label><input name="url" placeholder="mailto:hello@..." /></div>
          <button class="btn btn-primary" type="submit" style="grid-column: 1 / -1; justify-self: start">Add contact</button>
        </form>
      </div>
    `;
    bindRowActions(items, 'contacts', renderContacts, ['kind', 'label', 'value', 'url', 'icon']);
    $('#contactForm').addEventListener('submit', async (e) => {
      e.preventDefault();
      const f = e.target;
      const body = {
        kind: f.kind.value, label: f.label.value, value: f.value.value,
        url: f.url.value, icon: f.icon.value, order: items.length,
      };
      try { await api('POST', '/api/contacts', body); toast('added'); renderContacts(); }
      catch (err) { toast(err.message, true); }
    });
  }

  // ---------- section: skills (master/detail) ----------

  let activeClusterId = null;

  async function renderSkills() {
    const clusters = await api('GET', '/api/skill-clusters');
    if (activeClusterId == null && clusters.length) activeClusterId = clusters[0].id;
    const active = clusters.find(c => c.id === activeClusterId) || clusters[0] || null;
    const main = $('#main');
    main.innerHTML = `
      <h2>Skills</h2>
      <p class="lead">Five clusters from skills.yaml. Pick one to edit its tags.</p>
      <div class="master-detail">
        <div>
          <div class="card">
            <h3>Clusters</h3>
            <div class="master-list">${clusters.map(c => `
              <div class="item ${c.id === (active && active.id) ? 'active' : ''}" data-cluster-id="${c.id}">
                ${esc(c.title)}
                <div style="color:var(--fg-mute);font-size:11px;margin-top:2px">${esc(c.kicker)} · ${esc(c.accent || 'cyan')}</div>
              </div>`).join('')}</div>
          </div>
          <div class="card">
            <h3>New cluster</h3>
            <form id="newClusterForm">
              <div class="field"><label>kicker</label><input name="kicker" placeholder="// 06" /></div>
              <div class="field"><label>title</label><input name="title" required placeholder="Cluster name" /></div>
              <div class="field"><label>icon (lucide)</label><input name="icon" value="code-2" /></div>
              <div class="field"><label>accent</label>
                <select name="accent"><option value="">(cyan)</option><option value="accent-lime">lime</option><option value="accent-purple">purple</option></select>
              </div>
              <button class="btn btn-primary" type="submit">Add</button>
            </form>
          </div>
        </div>
        <div>
          ${active ? `
            <div class="card">
              <h3>Edit cluster · ${esc(active.title)}</h3>
              <form id="editClusterForm">
                <div class="grid-2">
                  <div class="field"><label>kicker</label><input name="kicker" value="${esc(active.kicker)}" /></div>
                  <div class="field"><label>title</label><input name="title" value="${esc(active.title)}" /></div>
                  <div class="field"><label>icon (lucide)</label><input name="icon" value="${esc(active.icon)}" /></div>
                  <div class="field"><label>accent</label>
                    <select name="accent">
                      <option value=""${active.accent === '' ? ' selected' : ''}>(cyan)</option>
                      <option value="accent-lime"${active.accent === 'accent-lime' ? ' selected' : ''}>lime</option>
                      <option value="accent-purple"${active.accent === 'accent-purple' ? ' selected' : ''}>purple</option>
                    </select>
                  </div>
                </div>
                <div style="display:flex;gap:8px;margin-top:8px">
                  <button class="btn btn-primary" type="submit">Save</button>
                  <button class="btn btn-danger" type="button" id="deleteClusterBtn">Delete cluster</button>
                </div>
              </form>
            </div>
            <div class="card">
              <h3>Tags</h3>
              <div id="tagPills">${(active.tags || []).map(t => `
                <span class="tag-pill">${esc(t.name)} <button data-tag-id="${t.id}" title="remove">×</button></span>
              `).join('') || '<span style="color:var(--fg-mute)">No tags yet.</span>'}</div>
              <form id="addTagForm" class="inline-form">
                <input name="name" required placeholder="new tag" />
                <button class="btn btn-primary" type="submit">Add tag</button>
              </form>
            </div>
          ` : '<div class="card"><h3>No cluster selected</h3></div>'}
        </div>
      </div>
    `;
    $$('.master-list .item').forEach(it => it.addEventListener('click', () => {
      activeClusterId = parseInt(it.dataset.clusterId, 10);
      renderSkills();
    }));
    $('#newClusterForm').addEventListener('submit', async (e) => {
      e.preventDefault();
      const f = e.target;
      const body = {
        kicker: f.kicker.value, title: f.title.value, icon: f.icon.value,
        accent: f.accent.value, order: clusters.length,
      };
      try {
        const created = await api('POST', '/api/skill-clusters', body);
        activeClusterId = created.id;
        toast('added'); renderSkills();
      } catch (err) { toast(err.message, true); }
    });
    if (active) {
      $('#editClusterForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const f = e.target;
        try {
          await api('PATCH', `/api/skill-clusters/${active.id}`, {
            kicker: f.kicker.value, title: f.title.value,
            icon: f.icon.value, accent: f.accent.value,
          });
          toast('saved'); renderSkills();
        } catch (err) { toast(err.message, true); }
      });
      $('#deleteClusterBtn').addEventListener('click', async () => {
        if (!confirm('Delete this cluster and all its tags?')) return;
        try {
          await api('DELETE', `/api/skill-clusters/${active.id}`);
          activeClusterId = null;
          toast('deleted'); renderSkills();
        } catch (err) { toast(err.message, true); }
      });
      $$('#tagPills button[data-tag-id]').forEach(btn => {
        btn.addEventListener('click', async () => {
          try {
            await api('DELETE', `/api/skill-tags/${btn.dataset.tagId}`);
            toast('removed'); renderSkills();
          } catch (err) { toast(err.message, true); }
        });
      });
      $('#addTagForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const name = e.target.name.value.trim();
        if (!name) return;
        try {
          await api('POST', `/api/skill-clusters/${active.id}/tags`,
                    { name, order: (active.tags || []).length });
          toast('added'); renderSkills();
        } catch (err) { toast(err.message, true); }
      });
    }
  }

  // ---------- section: projects ----------

  let activeProjectId = null;

  async function renderProjects() {
    const items = await api('GET', '/api/projects');
    if (activeProjectId == null && items.length) activeProjectId = items[0].id;
    const active = items.find(p => p.id === activeProjectId) || null;
    const main = $('#main');
    main.innerHTML = `
      <h2>Projects</h2>
      <p class="lead">Cards in the "Selected work" grid.</p>
      <div class="master-detail">
        <div>
          <div class="card">
            <h3>All projects</h3>
            <div class="master-list">${items.map(p => `
              <div class="item ${p.id === activeProjectId ? 'active' : ''}" data-project-id="${p.id}">
                ${esc(p.num || '')} ${esc(p.title)}
              </div>`).join('') || '<span style="color:var(--fg-mute)">No projects yet.</span>'}</div>
            <div style="display:flex;gap:6px;margin-top:8px">
              <button id="newProjectBtn" class="btn btn-primary btn-sm">+ new project</button>
            </div>
          </div>
        </div>
        <div>
          ${active ? `
            <div class="card">
              <h3>Edit · ${esc(active.title)}</h3>
              <form id="projectForm">
                <div class="grid-2">
                  <div class="field"><label>num</label><input name="num" value="${esc(active.num)}" placeholder="// 01" /></div>
                  <div class="field"><label>title</label><input name="title" value="${esc(active.title)}" required /></div>
                  <div class="field"><label>code url</label><input name="code_url" value="${esc(active.code_url)}" /></div>
                  <div class="field"><label>live url</label><input name="live_url" value="${esc(active.live_url)}" /></div>
                </div>
                <div class="field"><label>description</label><textarea name="description">${esc(active.description)}</textarea></div>
                <div style="display:flex;gap:8px;margin-top:8px">
                  <button class="btn btn-primary" type="submit">Save</button>
                  <button class="btn" type="button" id="upBtn">↑</button>
                  <button class="btn" type="button" id="downBtn">↓</button>
                  <button class="btn btn-danger" type="button" id="deleteBtn">Delete</button>
                </div>
              </form>
            </div>
            <div class="card">
              <h3>Tags</h3>
              <div id="ptags">${(active.tags || []).map(t => `
                <span class="tag-pill">${esc(t.name)} <button data-tag-id="${t.id}" title="remove">×</button></span>
              `).join('') || '<span style="color:var(--fg-mute)">No tags yet.</span>'}</div>
              <form id="addPtagForm" class="inline-form">
                <input name="name" required placeholder="new tag" />
                <button class="btn btn-primary" type="submit">Add tag</button>
              </form>
            </div>
          ` : '<div class="card"><h3>Select or create a project</h3></div>'}
        </div>
      </div>
    `;
    $$('.master-list .item[data-project-id]').forEach(it =>
      it.addEventListener('click', () => {
        activeProjectId = parseInt(it.dataset.projectId, 10);
        renderProjects();
      })
    );
    $('#newProjectBtn').addEventListener('click', async () => {
      try {
        const created = await api('POST', '/api/projects', {
          num: `// ${String(items.length + 1).padStart(2, '0')}`,
          title: 'New project', description: '', order: items.length,
        });
        activeProjectId = created.id;
        toast('created'); renderProjects();
      } catch (err) { toast(err.message, true); }
    });
    if (active) {
      $('#projectForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const f = e.target;
        try {
          await api('PATCH', `/api/projects/${active.id}`, {
            num: f.num.value, title: f.title.value,
            code_url: f.code_url.value, live_url: f.live_url.value,
            description: f.description.value,
          });
          toast('saved'); renderProjects();
        } catch (err) { toast(err.message, true); }
      });
      $('#deleteBtn').addEventListener('click', async () => {
        if (!confirm('Delete this project?')) return;
        try {
          await api('DELETE', `/api/projects/${active.id}`);
          activeProjectId = null; toast('deleted'); renderProjects();
        } catch (err) { toast(err.message, true); }
      });
      $('#upBtn').addEventListener('click', () => moveOrder(items, active, -1, 'projects', renderProjects));
      $('#downBtn').addEventListener('click', () => moveOrder(items, active, +1, 'projects', renderProjects));
      $$('#ptags button[data-tag-id]').forEach(btn => {
        btn.addEventListener('click', async () => {
          try { await api('DELETE', `/api/project-tags/${btn.dataset.tagId}`); toast('removed'); renderProjects(); }
          catch (err) { toast(err.message, true); }
        });
      });
      $('#addPtagForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const name = e.target.name.value.trim();
        if (!name) return;
        try {
          await api('POST', `/api/projects/${active.id}/tags`,
                    { name, order: (active.tags || []).length });
          toast('added'); renderProjects();
        } catch (err) { toast(err.message, true); }
      });
    }
  }

  // ---------- section: experience ----------

  let activeExpId = null;

  async function renderExperience() {
    const items = await api('GET', '/api/experience');
    if (activeExpId == null && items.length) activeExpId = items[0].id;
    const active = items.find(e => e.id === activeExpId) || null;
    const main = $('#main');
    main.innerHTML = `
      <h2>Experience</h2>
      <p class="lead">Timeline entries with bullet lists.</p>
      <div class="master-detail">
        <div>
          <div class="card">
            <h3>Entries</h3>
            <div class="master-list">${items.map(e => `
              <div class="item ${e.id === activeExpId ? 'active' : ''}" data-exp-id="${e.id}">
                ${esc(e.period)}<div style="color:var(--fg-mute);font-size:11px;margin-top:2px">${esc(e.role)}</div>
              </div>`).join('') || '<span style="color:var(--fg-mute)">No entries yet.</span>'}</div>
            <div style="margin-top:8px">
              <button id="newExpBtn" class="btn btn-primary btn-sm">+ new entry</button>
            </div>
          </div>
        </div>
        <div>
          ${active ? `
            <div class="card">
              <h3>Edit entry</h3>
              <form id="expForm">
                <div class="grid-2">
                  <div class="field"><label>period</label><input name="period" value="${esc(active.period)}" required placeholder="2024 — Present" /></div>
                  <div class="field"><label>role</label><input name="role" value="${esc(active.role)}" required /></div>
                  <div class="field"><label>company</label><input name="company" value="${esc(active.company)}" /></div>
                  <div class="field"><label>company meta</label><input name="company_meta" value="${esc(active.company_meta)}" placeholder="Ashgabat · full-time" /></div>
                </div>
                <div style="display:flex;gap:8px;margin-top:8px">
                  <button class="btn btn-primary" type="submit">Save</button>
                  <button class="btn" type="button" id="upBtn">↑</button>
                  <button class="btn" type="button" id="downBtn">↓</button>
                  <button class="btn btn-danger" type="button" id="deleteBtn">Delete</button>
                </div>
              </form>
            </div>
            <div class="card">
              <h3>Bullets</h3>
              <div class="row-list" id="bulletList">${(active.bullets || []).map(b => `
                <div class="row-item" data-bullet-id="${b.id}">
                  <div class="meta">${esc(b.text)}</div>
                  <div class="actions">
                    <button class="btn btn-sm" data-act="bedit">edit</button>
                    <button class="btn btn-sm btn-danger" data-act="bdel">del</button>
                  </div>
                </div>`).join('') || '<div class="meta sub">No bullets yet.</div>'}</div>
              <form id="addBulletForm" class="inline-form">
                <input name="text" required placeholder="new bullet" />
                <button class="btn btn-primary" type="submit">Add</button>
              </form>
            </div>
          ` : '<div class="card"><h3>Select or create an entry</h3></div>'}
        </div>
      </div>
    `;
    $$('.master-list .item[data-exp-id]').forEach(it =>
      it.addEventListener('click', () => {
        activeExpId = parseInt(it.dataset.expId, 10);
        renderExperience();
      })
    );
    $('#newExpBtn').addEventListener('click', async () => {
      try {
        const created = await api('POST', '/api/experience', {
          period: 'YYYY — YYYY', role: 'Role', company: 'Company',
          company_meta: '', order: items.length,
        });
        activeExpId = created.id;
        toast('created'); renderExperience();
      } catch (err) { toast(err.message, true); }
    });
    if (active) {
      $('#expForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const f = e.target;
        try {
          await api('PATCH', `/api/experience/${active.id}`, {
            period: f.period.value, role: f.role.value,
            company: f.company.value, company_meta: f.company_meta.value,
          });
          toast('saved'); renderExperience();
        } catch (err) { toast(err.message, true); }
      });
      $('#deleteBtn').addEventListener('click', async () => {
        if (!confirm('Delete this entry?')) return;
        try {
          await api('DELETE', `/api/experience/${active.id}`);
          activeExpId = null; toast('deleted'); renderExperience();
        } catch (err) { toast(err.message, true); }
      });
      $('#upBtn').addEventListener('click', () => moveOrder(items, active, -1, 'experience', renderExperience));
      $('#downBtn').addEventListener('click', () => moveOrder(items, active, +1, 'experience', renderExperience));
      $$('#bulletList .row-item').forEach(row => {
        const id = row.dataset.bulletId;
        row.querySelector('[data-act="bdel"]').addEventListener('click', async () => {
          if (!confirm('Delete bullet?')) return;
          try { await api('DELETE', `/api/experience-bullets/${id}`); toast('deleted'); renderExperience(); }
          catch (err) { toast(err.message, true); }
        });
        row.querySelector('[data-act="bedit"]').addEventListener('click', async () => {
          const current = row.querySelector('.meta').textContent.trim();
          const next = prompt('Edit bullet:', current);
          if (next == null) return;
          try { await api('PATCH', `/api/experience-bullets/${id}`, { text: next }); toast('saved'); renderExperience(); }
          catch (err) { toast(err.message, true); }
        });
      });
      $('#addBulletForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const text = e.target.text.value.trim();
        if (!text) return;
        try {
          await api('POST', `/api/experience/${active.id}/bullets`,
                    { text, order: (active.bullets || []).length });
          toast('added'); renderExperience();
        } catch (err) { toast(err.message, true); }
      });
    }
  }

  // ---------- shared row helpers ----------

  function bindRowActions(items, resource, refresh, editFields) {
    $$('#main .row-item').forEach(row => {
      const id = parseInt(row.dataset.id, 10);
      const item = items.find(x => x.id === id);
      if (!item) return;
      row.querySelector('[data-act="del"]')?.addEventListener('click', async () => {
        if (!confirm('Delete this row?')) return;
        try { await api('DELETE', `/api/${resource}/${id}`); toast('deleted'); refresh(); }
        catch (err) { toast(err.message, true); }
      });
      row.querySelector('[data-act="edit"]')?.addEventListener('click', async () => {
        const updates = {};
        for (const f of editFields) {
          const next = prompt(`Edit ${f}:`, item[f] || '');
          if (next == null) return;
          updates[f] = next;
        }
        try { await api('PATCH', `/api/${resource}/${id}`, updates); toast('saved'); refresh(); }
        catch (err) { toast(err.message, true); }
      });
      row.querySelector('[data-act="up"]')?.addEventListener('click', () => moveOrder(items, item, -1, resource, refresh));
      row.querySelector('[data-act="down"]')?.addEventListener('click', () => moveOrder(items, item, +1, resource, refresh));
    });
  }

  async function moveOrder(items, item, delta, resource, refresh) {
    const sorted = [...items].sort((a, b) => a.order - b.order || a.id - b.id);
    const idx = sorted.findIndex(x => x.id === item.id);
    const swapWith = sorted[idx + delta];
    if (!swapWith) return;
    try {
      await api('PATCH', `/api/${resource}/${item.id}`, { order: swapWith.order });
      await api('PATCH', `/api/${resource}/${swapWith.id}`, { order: item.order });
      refresh();
    } catch (err) { toast(err.message, true); }
  }

  // ---------- registry ----------

  const SECTIONS = {
    site: renderSite,
    stats: renderStats,
    contacts: renderContacts,
    skills: renderSkills,
    projects: renderProjects,
    experience: renderExperience,
  };

  // ---------- bootstrap ----------

  if (token()) {
    showDashboard();
  } else {
    showLogin();
  }
})();
