// blog.js
document.addEventListener("DOMContentLoaded", function() {
    console.log("JS بلاگ بارگذاری شد!");

    const postCards = document.querySelectorAll('.post-card');
    const buttons = document.querySelectorAll('.btn-primary, .read-more-btn');
    const badges = document.querySelectorAll('.tag-badge');

    // ===== کارت‌ها با انیمیشن ورود و Hover =====
    postCards.forEach((card, index) => {
        card.style.opacity = 0;
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'transform 0.6s cubic-bezier(0.22, 1, 0.36, 1), opacity 0.6s ease, box-shadow 0.4s ease';

        // ورود ترتیبی کارت‌ها با تاخیر ملایم
        setTimeout(() => {
            card.style.opacity = 1;
            card.style.transform = 'translateY(0)';
        }, 100 + index * 120);

        // افکت Hover کارت‌ها
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-10px)';
            card.style.boxShadow = '0 30px 60px rgba(0,0,0,0.25)';
        });
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0)';
            card.style.boxShadow = '0 10px 20px rgba(0,0,0,0.1)';
        });
    });

    // ===== دکمه‌ها با افکت Hover و کلیک =====
    buttons.forEach(btn => {
        // افکت کلیک
        btn.addEventListener('click', () => {
            btn.style.transform = 'scale(0.95)';
            setTimeout(() => { btn.style.transform = 'scale(1)'; }, 150);
        });

        // افکت Hover
        btn.addEventListener('mouseenter', () => {
            btn.style.transition = 'all 0.3s ease';
            btn.style.transform = 'translateY(-2px)';
        });
        btn.addEventListener('mouseleave', () => {
            btn.style.transform = 'translateY(0)';
        });
    });

    // ===== افکت Hover روی Badge ها =====
    badges.forEach(badge => {
        badge.style.transition = 'all 0.3s ease';
        badge.addEventListener('mouseenter', () => {
            badge.style.backgroundColor = '#0dcaf0';
            badge.style.color = '#000';
            badge.style.transform = 'scale(1.15)';
        });
        badge.addEventListener('mouseleave', () => {
            badge.style.backgroundColor = '';
            badge.style.color = '';
            badge.style.transform = 'scale(1)';
        });
    });

    // ===== ورود کارت‌ها هنگام اسکرول =====
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if(entry.isIntersecting) {
                entry.target.style.opacity = 1;
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.2 });

    postCards.forEach(card => observer.observe(card));

    // ===== محتوای داینامیک =====
    window.initDynamicContent = function() {
        postCards.forEach(card => observer.observe(card));
    };
});
