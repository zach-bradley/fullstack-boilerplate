<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-title>Home</ion-title>
        <ion-buttons slot="end">
          <ion-button @click="handleLogout">Logout</ion-button>
        </ion-buttons>
      </ion-toolbar>
    </ion-header>
    <ion-content class="ion-padding">
      <ion-card v-if="user">
        <ion-card-header>
          <ion-card-title>Welcome, {{ user.first_name }}!</ion-card-title>
        </ion-card-header>
        <ion-card-content>
          <ion-list>
            <ion-item>
              <ion-label>Email</ion-label>
              <ion-text>{{ user.email }}</ion-text>
            </ion-item>
            <ion-item>
              <ion-label>Name</ion-label>
              <ion-text>{{ user.first_name }} {{ user.last_name }}</ion-text>
            </ion-item>
          </ion-list>
        </ion-card-content>
      </ion-card>
    </ion-content>
  </ion-page>
</template>

<script lang="ts">
import { defineComponent, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../store/auth';
import {
  IonPage,
  IonHeader,
  IonToolbar,
  IonTitle,
  IonContent,
  IonButton,
  IonButtons,
  IonCard,
  IonCardHeader,
  IonCardTitle,
  IonCardContent,
  IonList,
  IonItem,
  IonLabel,
  IonText,
} from '@ionic/vue';

export default defineComponent({
  name: 'Home',
  components: {
    IonPage,
    IonHeader,
    IonToolbar,
    IonTitle,
    IonContent,
    IonButton,
    IonButtons,
    IonCard,
    IonCardHeader,
    IonCardTitle,
    IonCardContent,
    IonList,
    IonItem,
    IonLabel,
    IonText,
  },
  setup() {
    const router = useRouter();
    const authStore = useAuthStore();
    const user = computed(() => authStore.currentUser);

    const handleLogout = async () => {
      await authStore.logout();
      router.push('/login');
    };

    return {
      user,
      handleLogout,
    };
  },
});
</script> 