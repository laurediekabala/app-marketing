if (!window.dash_clientside) {
    window.dash_clientside = {};
}

window.dash_clientside.clientside = {
    update_theme_styles: function(theme_switch_value) {
        // ...existing code...
        const is_dark = theme_switch_value;
        const theme = is_dark ? 'dark' : 'light';

        const colors = {
            light: {
                background: '#f8f9fa',
                text: '#212529',
                sidebar: '#ffffff'
            },
            dark: {
                background: '#343a40',
                text: '#f8f9fa',
                sidebar: '#212529'
            }
        };

        const sidebar = document.getElementById('sidebar');
        const page_content = document.getElementById('page-content');

        if (sidebar && page_content) {
            sidebar.style.backgroundColor = colors[theme].sidebar;
            sidebar.style.color = colors[theme].text;

            page_content.style.backgroundColor = colors[theme].background;
            page_content.style.color = colors[theme].text;
        }

        return theme;
    }
};