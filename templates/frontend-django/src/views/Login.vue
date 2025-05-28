<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-title>Login</ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content class="ion-padding">
      <form @submit.prevent="handleSubmit">
        <ion-item>
          <ion-label position="floating">Email</ion-label>
          <ion-input
            type="email"
            v-model="form.email"
            required
          ></ion-input>
        </ion-item>

        <ion-item>
          <ion-label position="floating">Password</ion-label>
          <ion-input
            type="password"
            v-model="form.password"
            required
          ></ion-input>
        </ion-item>

        <ion-button
          expand="block"
          type="submit"
          :disabled="loading"
        >
          {{ loading ? 'Logging in...' : 'Login' }}
        </ion-button>

        <ion-text color="danger" v-if="error">
          <p>{{ error }}</p>
        </ion-text>

        <ion-button
          expand="block"
          fill="clear"
          router-link="/register"
        >
          Don't have an account? Register
        </ion-button>
      </form>
    </ion-content>
  </ion-page>
</template>

<script lang="ts">
import { defineComponent, reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../store/auth';
import {
  IonPage,
  IonHeader,
  IonToolbar,
  IonTitle,
  IonContent,
  IonItem,
  IonLabel,
  IonInput,
  IonButton,
  IonText,
} from '@ionic/vue';

export default defineComponent({
  name: 'Login',
  components: {
    IonPage,
    IonHeader,
    IonToolbar,
    IonTitle,
    IonContent,
    IonItem,
    IonLabel,
    IonInput,
    IonButton,
    IonText,
  },
  setup() {
    const router = useRouter();
    const authStore = useAuthStore();
    const loading = ref(false);
    const error = ref('');

    const form = reactive({
      email: '',
      password: '',
    });

    const handleSubmit = async () => {
      loading.value = true;
      error.value = '';

      try {
        await authStore.login(form);
        router.push('/');
      } catch (err: any) {
        error.value = err.message || 'Login failed';
      } finally {
        loading.value = false;
      }
    };

    return {
      form,
      loading,
      error,
      handleSubmit,
    };
  },
});
</script> 