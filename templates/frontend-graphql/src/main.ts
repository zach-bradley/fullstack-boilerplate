import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';
import { IonicVue } from '@ionic/vue';
import './global.scss';
import '@ionic/core/css/ionic.bundle.css';
import '@ionic/vue/css/core.css';
import '@ionic/vue/css/normalize.css';
import '@ionic/vue/css/structure.css';
import '@ionic/vue/css/typography.css';
import '@ionic/vue/css/padding.css';
import '@ionic/vue/css/float-elements.css';
import '@ionic/vue/css/text-alignment.css';
import '@ionic/vue/css/text-transformation.css';
import '@ionic/vue/css/flex-utils.css';
import '@ionic/vue/css/display.css';
import { useMainStore } from './store';

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(router);
app.use(IonicVue);

// Initialize authentication state
const store = useMainStore();
store.initializeAuth();

router.isReady().then(() => {
    app.mount('#app');
});
