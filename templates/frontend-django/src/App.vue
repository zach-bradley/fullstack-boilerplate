<template>
  <ion-app>
    <ion-router-outlet />
  </ion-app>
</template>

<script lang="ts">
import { defineComponent, onMounted } from 'vue';
import { IonApp, IonRouterOutlet } from '@ionic/vue';
import { useAuthStore } from './store/auth';

export default defineComponent({
  name: 'App',
  components: {
    IonApp,
    IonRouterOutlet,
  },
  setup() {
    const authStore = useAuthStore();

    onMounted(async () => {
      if (authStore.isAuthenticated) {
        try {
          await authStore.fetchProfile();
        } catch (error) {
          authStore.logout();
        }
      }
    });
  },
});
</script>

<style>
ion-content {
  --background: var(--ion-color-light);
}
</style> 