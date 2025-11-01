document.addEventListener('DOMContentLoaded', function() {
    initBlog();
});

function initBlog() {
    initCardHover();
    initLikeButtons();
    initSearch();
}

// افکت hover روی کارت‌ها
function initCardHover() {
    const cards = document.querySelectorAll('.post-card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-10px)';
            card.style.zIndex = '10';
        });
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0)';
            card.style.zIndex = '1';
        });
    });
}

// دکمه لایک با localStorage
function initLikeButtons() {
    const likeButtons = document.querySelectorAll('.stat-item');
    likeButtons.forEach(button => {
        const postId = button.getAttribute('data-post-id');
        if (postId && localStorage.getItem(`liked_${postId}`)) {
            button.classList.add('liked');
            button.innerHTML = '<i class="bi bi-heart-fill"></i>';
        }
        button.addEventListener('click', () => {
            button.classList.toggle('liked');
            if (button.classList.contains('liked')) {
                button.innerHTML = '<i class="bi bi-heart-fill"></i>';
                if (postId) localStorage.setItem(`liked_${postId}`, 'true');
            } else {
                button.innerHTML = '<i class="bi bi-heart"></i>';
                if (postId) localStorage.removeItem(`liked_${postId}`);
            }
        });
    });
}

// جستجو بین پست‌ها
function initSearch() {
    const input = document.querySelector('.search-box input');
    if (!input) return;

    input.addEventListener('keyup', function() {
        const term = input.value.trim().toLowerCase();
        const cards = document.querySelectorAll('.post-card');

        cards.forEach(card => {
            const title = card.querySelector('.card-title').textContent.toLowerCase();
            const text = card.querySelector('.card-text').textContent.toLowerCase();
            if (title.includes(term) || text.includes(term)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    });
}
