<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-title>My Lists</ion-title>
        <ion-buttons slot="end">
          <ion-button @click="handleLogout" color="danger">
            <ion-icon :icon="logOutOutline"></ion-icon>
          </ion-button>
        </ion-buttons>
      </ion-toolbar>
    </ion-header>

    <ion-content>
      <ion-refresher slot="fixed" @ionRefresh="handleRefresh($event)">
        <ion-refresher-content></ion-refresher-content>
      </ion-refresher>

      <div class="ion-padding">
        <div class="ion-text-center ion-padding">
          <ion-icon :icon="listOutline" style="font-size: 48px; color: var(--ion-color-medium)"></ion-icon>
          <p class="ion-text-center ion-padding-top">Ready to start building?</p>
        </div>

        <!-- Error State -->
        <ion-card v-if="error" color="danger">
          <ion-card-content>
            <ion-text color="light">{{ error }}</ion-text>
          </ion-card-content>
        </ion-card>
      </div>
    </ion-content>
  </ion-page>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, computed } from "vue";
import { useIonRouter } from '@ionic/vue';
import {
  IonPage,
  IonContent,
  IonButton,
  IonCard,
  IonText,
  IonCardHeader,
  IonCardTitle,
  IonCardContent,
  IonItem,
  IonInput,
  IonList,
  IonLabel,
  IonIcon,
  IonHeader,
  IonToolbar,
  IonTitle,
  IonButtons,
  IonRefresher,
  IonRefresherContent,
  IonSpinner,
  IonModal
} from '@ionic/vue';
import {
  chevronForward,
  logOutOutline,
  listOutline,
  addOutline,
  closeOutline
} from 'ionicons/icons';
import { useMainStore } from '../store';

export default defineComponent({
  name: 'HomePage',
  components: {
    IonPage,
    IonContent,
    IonButton,
    IonCard,
    IonText,
    IonCardHeader,
    IonCardTitle,
    IonCardContent,
    IonItem,
    IonInput,
    IonList,
    IonLabel,
    IonIcon,
    IonHeader,
    IonToolbar,
    IonTitle,
    IonButtons,
    IonRefresher,
    IonRefresherContent,
    IonSpinner,
    IonModal
  },
  setup() {
    const store = useMainStore();
    const router = useIonRouter();
    
    const isLoading = computed(() => store.isLoading);
    const error = computed(() => store.error);
    const username = computed(() => store.username);

    const handleRefresh = async (event: any) => {
      event.target.complete();
    };
    
    const handleLogout = async () => {
      try {
        const response = await fetch('/api/logout', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          }
        });
        if (response.ok) {
          store.logout();
          router.push('/auth');
        } else {
          console.error('Logout failed:', response.statusText);
        }
      } catch (error) {
        console.error('Logout error:', error);
      }
    };

    onMounted(() => {
    });

    return {
      username,
      isLoading,
      error,
      handleLogout,
      handleRefresh,
      chevronForward,
      logOutOutline,
      listOutline,
      addOutline,
      closeOutline
    };
  }
});
</script>

<style scoped>
.align-items {
  display: flex;
  align-items: center;
  justify-content: center;
}
h1 {
  margin: 0;
  font-size: 36px;
}
.full-height {
  height: 100%;
}
ion-card {
  background-color: var(--ion-card-background-color); 
  padding: 10px;
}
ion-col {
 margin: auto;
}
ion-card-title , ion-card-subtitle {
  text-align: center;
}
</style>
