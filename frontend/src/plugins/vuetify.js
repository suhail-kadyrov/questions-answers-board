// Styles
import "@mdi/font/css/materialdesignicons.css";
import "vuetify/styles";

// Vuetify
import { createVuetify } from "vuetify";

const customTheme = {
    dark: false,
    colors: {
        background: '#929D94',
        surface: '#065342',
        primary: '#065342',
        //   'primary-darken-1': '#3700B3',
        secondary: '#FBF7F5',
        //   'secondary-darken-1': '#018786',
        error: '#E53935',
        info: '#2196F3',
        success: '#4CAF50',
        warning: '#F5C329',
    }
}

export default createVuetify({
    theme: {
        defaultTheme: 'customTheme',
        themes: {
            customTheme,
        }
    }
})

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
