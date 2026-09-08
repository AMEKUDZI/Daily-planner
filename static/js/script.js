'use strict';

document.addEventListener('DOMContentLoaded', () => {

    /* --- Flash auto-dismiss --- */
    document.querySelectorAll('.flash').forEach(el => {
        setTimeout(() => {
            el.style.transition = 'opacity .35s ease, transform .35s ease';
            el.style.opacity = '0';
            el.style.transform = 'translateY(-5px)';
            setTimeout(() => el.remove(), 360);
        }, 4500);
    });

    /* --- Mobile drawer --- */
    const overlay = document.getElementById('drawerOverlay');
    const drawer  = document.getElementById('drawer');
    const openBtn = document.getElementById('menuOpen');
    const closeBtn= document.getElementById('menuClose');

    const openDrawer  = () => { overlay?.classList.add('open'); drawer?.classList.add('open'); document.body.style.overflow = 'hidden'; };
    const closeDrawer = () => { overlay?.classList.remove('open'); drawer?.classList.remove('open'); document.body.style.overflow = ''; };

    openBtn?.addEventListener('click', openDrawer);
    closeBtn?.addEventListener('click', closeDrawer);
    overlay?.addEventListener('click', closeDrawer);

    /* --- Notify option cards --- */
    document.querySelectorAll('.notify-opt').forEach(card => {
        const cb = card.querySelector('input[type="checkbox"]');
        if (!cb) return;
        const sync = () => card.classList.toggle('checked', cb.checked);
        sync();
        card.addEventListener('click', () => { cb.checked = !cb.checked; sync(); });
    });

    /* --- Live clock on dashboard --- */
    const clock = document.getElementById('liveClock');
    if (clock) {
        const tick = () => {
            const now = new Date();
            clock.textContent = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        };
        tick();
        setInterval(tick, 1000);
    }

});
