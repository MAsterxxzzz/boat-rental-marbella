(function(){
  function fire(name, params){
    if (typeof gtag === 'function') { gtag('event', name, params || {}); }
  }

  document.addEventListener('click', function(e){
    var wa = e.target.closest('a[href*="wa.me"]');
    if (wa) { fire('whatsapp_click', {link_url: wa.href}); return; }

    var mail = e.target.closest('a[href^="mailto:"]');
    if (mail) { fire('email_click', {link_url: mail.href}); return; }

    if (e.target.closest('[data-open-book]')) { fire('booking_started', {}); }
  }, true);

  document.addEventListener('submit', function(e){
    var f = e.target;
    if (f && f.id === 'bookForm') {
      fire('booking_form_submit', {
        boat: (f.boat && f.boat.value) || '',
        guests: (f.guests && f.guests.value) || '',
        has_date: !!(f.date && f.date.value)
      });
    }
  }, true);
})();
