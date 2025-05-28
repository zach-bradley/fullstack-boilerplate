<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-title>Register</ion-title>
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
          <ion-label position="floating">First Name</ion-label>
          <ion-input
            type="text"
            v-model="form.first_name"
            required
          ></ion-input>
        </ion-item>

        <ion-item>
          <ion-label position="floating">Last Name</ion-label>
          <ion-input
            type="text"
            v-model="form.last_name"
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

        <ion-item>
          <ion-label position="floating">Confirm Password</ion-label>
          <ion-input
            type="password"
            v-model="form.password2"
            required
          ></ion-input>
        </ion-item>

        <ion-button
          expand="block"
          type="submit"
          :disabled="loading"
        >
          {{ loading ? 'Registering...' : 'Register' }}
        </ion-button>

        <ion-text color="danger" v-if="error">
          <p>{{ error }}</p>
        </ion-text>

        <ion-button
          expand="block"
          fill="clear"
          router-link="/login"
        >
          Already have an account? Login
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
  name: 'Register',
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
      first_name: '',
      last_name: '',
      password: '',
      password2: '',
    });

    const handleSubmit = async () => {
      if (form.password !== form.password2) {
        error.value = 'Passwords do not match';
        return;
      }

      loading.value = true;
      error.value = '';

      try {
        await authStore.register(form);
        router.push('/');
      } catch (err: any) {
        error.value = err.message || 'Registration failed';
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