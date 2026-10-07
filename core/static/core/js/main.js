(function () {
  'use strict';

  // Icons
  if (window.lucide) {
    window.lucide.createIcons();
  }

  var header = document.getElementById('siteHeader');
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('siteNav');

  // Header shadow once the page scrolls
  function onScroll() {
    if (header) header.classList.toggle('is-scrolled', window.scrollY > 20);
  }
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  // Mobile menu
  function closeMenu() {
    if (!toggle || !nav) return;
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'Open menu');
    nav.classList.remove('is-open');
  }

  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!open));
      toggle.setAttribute('aria-label', open ? 'Open menu' : 'Close menu');
      nav.classList.toggle('is-open', !open);
    });
    nav.addEventListener('click', function (event) {
      if (event.target.closest('a')) closeMenu();
    });
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape') closeMenu();
    });
    document.addEventListener('click', function (event) {
      if (!event.target.closest('.navbar')) closeMenu();
    });
  }

  if (!('IntersectionObserver' in window)) return;

  // Highlight the menu link of the section in view
  var navLinks = Array.prototype.slice.call(document.querySelectorAll('.nav__links a[href^="#"]'));
  var linkFor = {};
  navLinks.forEach(function (link) {
    linkFor[link.getAttribute('href').slice(1)] = link;
  });
  var sectionObserver = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      var link = linkFor[entry.target.id];
      if (!link || !entry.isIntersecting) return;
      navLinks.forEach(function (other) { other.classList.remove('is-active'); });
      link.classList.add('is-active');
    });
  }, { rootMargin: '-45% 0px -50% 0px' });
  Object.keys(linkFor).forEach(function (id) {
    var section = document.getElementById(id);
    if (section) sectionObserver.observe(section);
  });

  // Floating buttons stay visible until the footer comes into view
  var floating = document.getElementById('floatingButtons');
  var footer = document.getElementById('siteFooter');
  if (floating && footer) {
    new IntersectionObserver(function (entries) {
      floating.classList.toggle('is-hidden', entries[0].isIntersecting);
    }, { threshold: 0.05 }).observe(footer);
  }

  // Fade-up on scroll
  var revealItems = document.querySelectorAll('[data-reveal]');
  if (revealItems.length) {
    document.documentElement.classList.add('js-reveal');
    var revealObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-visible');
        revealObserver.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    revealItems.forEach(function (item, index) {
      // small stagger for items that appear together
      item.style.transitionDelay = (index % 4) * 0.08 + 's';
      revealObserver.observe(item);
    });
  }
})();
