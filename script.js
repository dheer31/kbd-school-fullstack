// ===== API CONFIG =====
// Docker / Vercel / Production → nginx proxies /api/* → FastAPI (relative URL)
// Local dev without Docker (e.g. served on :8888 / :5500) → call FastAPI directly on :8000
const _isLocalDev = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
  && window.location.port !== ''
  && window.location.port !== '80'
  && window.location.port !== '443';
const API_BASE = _isLocalDev ? 'http://localhost:8000' : '';

// ===== NAVBAR SCROLL & ACTIVE =====
const navbar = document.getElementById('navbar');
const navLinks = document.querySelectorAll('.nav-link');
const sections = document.querySelectorAll('section[id]');
const tickerBar = document.getElementById('ticker-bar');

let lastScrollY = window.scrollY;

window.addEventListener('scroll', () => {
  const scrollY = window.scrollY;

  // Navbar scroll class
  if (scrollY > 80) {
    navbar.classList.add('scrolled');
    if (scrollY > lastScrollY) {
      tickerBar.style.transform = 'translateY(-100%)';
    } else {
      tickerBar.style.transform = 'translateY(0)';
    }
  } else {
    navbar.classList.remove('scrolled');
    tickerBar.style.transform = 'translateY(0)';
  }
  lastScrollY = scrollY;

  // Active nav link
  let current = '';
  sections.forEach(section => {
    const sectionTop = section.offsetTop - 140;
    if (scrollY >= sectionTop) {
      current = section.getAttribute('id');
    }
  });
  navLinks.forEach(link => {
    link.classList.remove('active');
    if (link.getAttribute('href') === `#${current}`) {
      link.classList.add('active');
    }
  });

  // Back to top
  const btn = document.getElementById('back-to-top');
  if (scrollY > 400) {
    btn.classList.add('visible');
  } else {
    btn.classList.remove('visible');
  }

  // Reveal on scroll
  document.querySelectorAll('.reveal').forEach(el => {
    const rect = el.getBoundingClientRect();
    if (rect.top < window.innerHeight - 80) {
      el.classList.add('visible');
    }
  });
});

// Apply reveal classes to elements
document.addEventListener('DOMContentLoaded', () => {
  const revealTargets = [
    '.about-grid',
    '.subject-card',
    '.facility-card',
    '.step',
    '.faculty-card',
    '.gallery-item',
    '.news-card',
    '.contact-card',
    '.quick-item',
    '.value-card',
    '.principal-card',
    '.admission-form-card',
    '.admission-eligibility',
    '.admission-steps',
    '.section-header'
  ];

  revealTargets.forEach(selector => {
    document.querySelectorAll(selector).forEach((el, i) => {
      el.classList.add('reveal');
      el.style.transitionDelay = `${i * 0.07}s`;
    });
  });

  // Trigger once on load
  setTimeout(() => {
    document.querySelectorAll('.reveal').forEach(el => {
      const rect = el.getBoundingClientRect();
      if (rect.top < window.innerHeight - 80) {
        el.classList.add('visible');
      }
    });
  }, 100);
});

// ===== HAMBURGER =====
const hamburger = document.getElementById('hamburger');
const navLinksContainer = document.getElementById('nav-links');

hamburger.addEventListener('click', () => {
  hamburger.classList.toggle('open');
  navLinksContainer.classList.toggle('open');
});

navLinks.forEach(link => {
  link.addEventListener('click', () => {
    hamburger.classList.remove('open');
    navLinksContainer.classList.remove('open');
  });
});

// ===== COUNTER ANIMATION =====
function animateCounter(el) {
  const target = parseInt(el.getAttribute('data-target'));
  const duration = 2000;
  const start = performance.now();

  function update(currentTime) {
    const elapsed = currentTime - start;
    const progress = Math.min(elapsed / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    el.textContent = Math.floor(eased * target);
    if (progress < 1) requestAnimationFrame(update);
    else el.textContent = target;
  }
  requestAnimationFrame(update);
}

const counters = document.querySelectorAll('.stat-number');
let countersStarted = false;

const counterObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting && !countersStarted) {
      countersStarted = true;
      counters.forEach(counter => animateCounter(counter));
    }
  });
}, { threshold: 0.5 });

const heroStats = document.querySelector('.hero-stats');
if (heroStats) counterObserver.observe(heroStats);

// ===== ACADEMICS TABS =====
const tabBtns = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');

tabBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    const target = btn.getAttribute('data-tab');
    tabBtns.forEach(b => b.classList.remove('active'));
    tabContents.forEach(c => c.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById(`tab-content-${target}`).classList.add('active');
  });
});

// ===== GALLERY FILTER =====
const filterBtns = document.querySelectorAll('.filter-btn');
const galleryItems = document.querySelectorAll('.gallery-item');

filterBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    const filter = btn.getAttribute('data-filter');
    filterBtns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    galleryItems.forEach(item => {
      const category = item.getAttribute('data-category');
      if (filter === 'all' || category === filter) {
        item.style.display = 'block';
        item.style.animation = 'fade-up 0.4s ease forwards';
      } else {
        item.style.display = 'none';
      }
    });
  });
});

// ===== LIGHTBOX =====
const lightbox = document.getElementById('lightbox');
const lightboxContent = document.getElementById('lightbox-content');
const lightboxClose = document.getElementById('lightbox-close');

galleryItems.forEach(item => {
  item.addEventListener('click', () => {
    const img = item.querySelector('img');
    if (img) {
      lightboxContent.innerHTML = `<img src="${img.src}" alt="${img.alt}" />`;
      lightbox.classList.add('active');
      document.body.style.overflow = 'hidden';
    }
  });
});

lightboxClose.addEventListener('click', closeLightbox);
lightbox.addEventListener('click', (e) => { if (e.target === lightbox) closeLightbox(); });
document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeLightbox(); });

function closeLightbox() {
  lightbox.classList.remove('active');
  document.body.style.overflow = '';
  lightboxContent.innerHTML = '';
}

// ===== ADMISSION FORM — Connected to FastAPI =====
const admissionForm = document.getElementById('admission-form');
const formSuccess = document.getElementById('form-success');

admissionForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const btn = admissionForm.querySelector('button[type="submit"]');
  btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Submitting...';
  btn.disabled = true;

  const payload = {
    student_name: document.getElementById('student-name').value.trim(),
    dob:          document.getElementById('dob').value,
    applying_class: document.getElementById('applying-class').value,
    parent_name:  document.getElementById('parent-name').value.trim(),
    phone:        document.getElementById('phone').value.trim(),
    email:        document.getElementById('email').value.trim() || null,
  };

  try {
    const res = await fetch(`${API_BASE}/api/admissions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    if (!res.ok) throw new Error(`Server error: ${res.status}`);

    admissionForm.classList.add('hidden');
    formSuccess.classList.remove('hidden');
  } catch (err) {
    console.error('Submission failed:', err);
    btn.innerHTML = '<i class="fas fa-exclamation-circle"></i> Submission Failed — Try Again';
    btn.disabled = false;
    btn.style.background = 'linear-gradient(135deg, #e63946, #c1121f)';
  }
});

// ===== LOAD DYNAMIC EVENTS FROM API =====
async function loadEventsFromAPI() {
  try {
    const res = await fetch(`${API_BASE}/api/events`);
    if (!res.ok) return;
    const { data: events } = await res.json();
    if (!events || events.length === 0) return;

    const grid = document.getElementById('gallery-grid');
    if (!grid) return;

    const categoryColors = {
      events:   'linear-gradient(135deg, #1a3d7c, #4e88d9)',
      trips:    'linear-gradient(135deg, #2d6a4f, #74c69d)',
      sports:   'linear-gradient(135deg, #e63946, #f4a261)',
      academic: 'linear-gradient(135deg, #7b2d8b, #da77f2)',
    };
    const categoryIcons = {
      events:   'fa-calendar-star',
      trips:    'fa-map-marked-alt',
      sports:   'fa-trophy',
      academic: 'fa-graduation-cap',
    };

    events.forEach(event => {
      const item = document.createElement('div');
      item.className = 'gallery-item';
      item.setAttribute('data-category', event.category || 'events');

      if (event.image_url) {
        item.innerHTML = `
          <img src="${event.image_url}" alt="${event.title}" />
          <div class="gallery-overlay">
            <i class="fas fa-expand"></i>
            <span>${event.title}</span>
          </div>`;
      } else {
        const bg = categoryColors[event.category] || categoryColors.events;
        const icon = categoryIcons[event.category] || 'fa-star';
        item.innerHTML = `
          <div class="gallery-placeholder" style="background: ${bg};">
            <i class="fas ${icon}"></i>
            <span>${event.title}</span>
          </div>
          <div class="gallery-overlay">
            <i class="fas fa-expand"></i>
            <span>${event.title}${event.date ? ' — ' + event.date : ''}</span>
          </div>`;
      }

      // Add lightbox click
      item.addEventListener('click', () => {
        const img = item.querySelector('img');
        if (img) {
          lightboxContent.innerHTML = `<img src="${img.src}" alt="${img.alt}" />`;
          lightbox.classList.add('active');
          document.body.style.overflow = 'hidden';
        }
      });

      grid.appendChild(item);
    });

    // Re-apply gallery filter to include new items
    const activeFilter = document.querySelector('.filter-btn.active');
    if (activeFilter && activeFilter.getAttribute('data-filter') !== 'all') {
      activeFilter.click();
    }
  } catch (err) {
    console.warn('Could not load events from API:', err.message);
  }
}

// ===== FACULTY FROM API =====
async function loadFaculty() {
  const leaderBanner  = document.getElementById('leadership-banner');
  const facultyGrid   = document.getElementById('faculty-grid-dynamic');
  if (!leaderBanner || !facultyGrid) return;

  try {
    const res  = await fetch(`${API_BASE}/api/faculty`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const json = await res.json();
    const members = json.data || [];

    const leaders  = members.filter(m => m.is_leader);
    const teachers = members.filter(m => !m.is_leader);

    // ── Leadership banner ────────────────────────────────────────────────────
    if (leaders.length === 0) {
      leaderBanner.innerHTML = '';
    } else {
      const leaderCards = leaders.map((m, idx) => {
        const divider = idx < leaders.length - 1
          ? `<div class="leader-divider"><i class="fas fa-school"></i></div>`
          : '';
        const cls = m.avatar_class ? ` leader-${m.avatar_class.replace('fa-', '')}` : '';
        return `
          <div class="leader-card${cls}">
            <div class="leader-icon"><i class="${m.icon}"></i></div>
            <div class="leader-details">
              <div class="leader-label">${m.role}</div>
              <h3 class="leader-name">${m.name}</h3>
              <p class="leader-since">${m.qualification || ''}</p>
            </div>
          </div>${divider}`;
      }).join('');
      leaderBanner.innerHTML = leaderCards;
    }

    // ── Teacher cards ────────────────────────────────────────────────────────
    if (teachers.length === 0) {
      facultyGrid.innerHTML = '<p class="faculty-empty">No teachers added yet.</p>';
    } else {
      facultyGrid.innerHTML = teachers.map(m => {
        const avatarCls = m.avatar_class ? ` ${m.avatar_class}` : '';
        return `
          <div class="faculty-card">
            <div class="faculty-avatar${avatarCls}"><i class="${m.icon}"></i></div>
            <div class="faculty-info">
              <h4>${m.name}</h4>
              <span class="faculty-role">${m.role}</span>
              <p>${m.qualification ? `${m.qualification} | ` : ''}${m.bio || ''}</p>
            </div>
          </div>`;
      }).join('');
    }

  } catch (err) {
    console.warn('Could not load faculty from API:', err.message);
    // Fallback — hide the loading spinner silently
    leaderBanner.innerHTML = '';
    facultyGrid.innerHTML  = '';
  }
}

// ===== NEWS FROM API =====
async function loadNews() {
  const grid = document.getElementById('news-grid');
  const loading = document.getElementById('news-loading');
  if (!grid) return;

  // Tag colour map — matches CSS .news-tag variants
  const tagClass = {
    featured : 'featured',
    new      : 'new',
    upcoming : '',
    notice   : '',
  };

  try {
    const res = await fetch(`${API_BASE}/api/news`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const { data: items } = await res.json();

    if (loading) loading.remove();

    if (!items || items.length === 0) {
      grid.innerHTML = '<p class="news-empty">No news items yet.</p>';
      return;
    }

    grid.innerHTML = items.map(item => {
      const cls = item.is_featured ? 'news-card featured' : 'news-card';
      const tagKey = (item.tag || '').toLowerCase();
      const tagCls = tagClass[tagKey] !== undefined ? tagClass[tagKey] : '';
      const tagHTML = tagCls
        ? `<div class="news-tag ${tagCls}">${item.tag}</div>`
        : `<div class="news-tag">${item.tag}</div>`;
      const dateHTML = item.date
        ? `<div class="news-date"><i class="fas fa-calendar-alt"></i> ${item.date}</div>`
        : '';
      const link = item.link || '#';
      const linkText = item.link_text || 'Read More';
      return `
        <div class="${cls}">
          ${tagHTML}
          ${dateHTML}
          <h3>${item.title}</h3>
          <p>${item.description || ''}</p>
          <a href="${link}" class="news-link">${linkText} <i class="fas fa-arrow-right"></i></a>
        </div>`;
    }).join('');

    // Re-apply reveal animation to new cards
    grid.querySelectorAll('.news-card').forEach((el, i) => {
      el.classList.add('reveal');
      el.style.transitionDelay = `${i * 0.07}s`;
      const rect = el.getBoundingClientRect();
      if (rect.top < window.innerHeight - 80) el.classList.add('visible');
    });

  } catch (err) {
    console.warn('Could not load news from API:', err.message);
    if (loading) loading.innerHTML =
      '<i class="fas fa-exclamation-circle"></i> Could not load news.';
  }
}

// Load API events + faculty + news when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  loadEventsFromAPI();
  loadFaculty();
  loadNews();
});


// ===== BACK TO TOP =====
document.getElementById('back-to-top').addEventListener('click', () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
});

// ===== SMOOTH ANCHOR SCROLL =====
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    const href = this.getAttribute('href');
    if (href === '#') return;
    const target = document.querySelector(href);
    if (target) {
      e.preventDefault();
      const offset = 120;
      const top = target.getBoundingClientRect().top + window.scrollY - offset;
      window.scrollTo({ top, behavior: 'smooth' });
    }
  });
});

// ===== TICKER PAUSE ON HOVER =====
const tickerContent = document.querySelector('.ticker-content');
if (tickerContent) {
  tickerContent.addEventListener('mouseenter', () => {
    tickerContent.style.animationPlayState = 'paused';
  });
  tickerContent.addEventListener('mouseleave', () => {
    tickerContent.style.animationPlayState = 'running';
  });
}

console.log('%c🏫 K.B.D. English Medium School Website Loaded!', 'color: #1a3d7c; font-size: 16px; font-weight: bold;');
