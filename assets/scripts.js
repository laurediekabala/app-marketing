if (!window.dash_clientside) {
    window.dash_clientside = {};
}

window.dash_clientside.clientside = {
    update_theme_styles: function(theme_switch_value) {
        // Empêcher les appels multiples rapides
        if (window.theme_updating) {
            return window.dash_clientside.no_update;
        }
        
        window.theme_updating = true;
        
        setTimeout(() => {
            window.theme_updating = false;
        }, 500);

        const is_dark = theme_switch_value;
        const theme = is_dark ? 'dark' : 'light';

        // Définition des couleurs
        const colors = {
            light: {
                sidebar_bg: '#f8f9fa',
                content_bg: '#ffffff',
                text: '#212529',
                border: '#dee2e6',
                card_bg: '#ffffff',
                secondary_bg: '#e9ecef'
            },
            dark: {
                sidebar_bg: '#212529',
                content_bg: '#1a1a1a',
                text: '#f8f9fa', 
                border: '#495057',
                card_bg: '#343a40',
                secondary_bg: '#495057'
            }
        };

        const currentColors = colors[theme];

        // Mettre à jour la sidebar
        const sidebar = document.getElementById('sidebar');
        if (sidebar) {
            sidebar.style.backgroundColor = currentColors.sidebar_bg;
            sidebar.style.color = currentColors.text;
            sidebar.style.borderRight = `1px solid ${currentColors.border}`;
            
            // Mettre à jour les éléments de la sidebar
            const bgLightElements = sidebar.querySelectorAll('.bg-light');
            bgLightElements.forEach(element => {
                if (is_dark) {
                    element.style.backgroundColor = currentColors.secondary_bg;
                    element.style.color = currentColors.text;
                } else {
                    element.style.backgroundColor = '#e9ecef';
                    element.style.color = currentColors.text;
                }
            });

            // Mettre à jour les liens de navigation
            const navLinks = sidebar.querySelectorAll('.nav-link');
            navLinks.forEach(link => {
                link.style.color = currentColors.text;
            });
        }

        // Mettre à jour le contenu principal
        const page_content = document.getElementById('page-content');
        if (page_content) {
            page_content.style.backgroundColor = currentColors.content_bg;
            page_content.style.color = currentColors.text;
            
            // Mettre à jour les cartes dans le contenu principal
            const contentCards = page_content.querySelectorAll('.card');
            contentCards.forEach(card => {
                card.style.backgroundColor = currentColors.card_bg;
                card.style.color = currentColors.text;
                card.style.borderColor = currentColors.border;
            });

            // Mettre à jour les alertes
            const alerts = page_content.querySelectorAll('.alert');
            alerts.forEach(alert => {
                if (is_dark) {
                    alert.style.backgroundColor = currentColors.card_bg;
                    alert.style.borderColor = currentColors.border;
                }
            });
        }

        // Sauvegarder la préférence dans le localStorage
        localStorage.setItem('theme_preference', theme);
        
        return theme;
    }
};

// Charger le thème au démarrage de la page
document.addEventListener('DOMContentLoaded', function() {
    const saved_theme = localStorage.getItem('theme_preference') || 'light';
    const theme_switch = document.getElementById('theme-switch');
    
    if (theme_switch && saved_theme === 'dark') {
        // Petit délai pour s'assurer que Dash est initialisé
        setTimeout(() => {
            theme_switch.checked = true;
            // Déclencher manuellement la mise à jour du thème
            window.dash_clientside.clientside.update_theme_styles(true);
        }, 100);
    }
});