<template>
  <ion-app>
    <ion-menu content-id="main-content" type="overlay" v-if="this.store.isAuthenticated">
      <ion-content>
        <ion-list id="inbox-list">
          <ion-list-header>RemindMe</ion-list-header>
          <ion-note>hi@ionicframework.com</ion-note>

          <ion-menu-toggle auto-hide="false" v-for="(p, i) in appPages" :key="i">
            <ion-item @click="selectedIndex = i" router-link :to="p.url" lines="none" detail="false" class="hydrated" :class="{ selected: selectedIndex === i }">
              <ion-icon :icon="p.icon" slot="start"></ion-icon>
              <ion-label>{{ p.title }}</ion-label>
            </ion-item>
          </ion-menu-toggle>
        </ion-list>
      </ion-content>
    </ion-menu>
    <div class="ion-page" id="main-content">
      <ion-header>
        <ion-toolbar>
          <ion-buttons slot="start">
            <ion-menu-button></ion-menu-button>
          </ion-buttons>
        </ion-toolbar>
      </ion-header>
      <ion-content :fullscreen="true">
        <ion-router-outlet></ion-router-outlet>
      </ion-content>
    </div>
  </ion-app>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from "vue";
import { 
  IonApp, 
  IonRouterOutlet, 
  IonMenu,
  IonHeader,
  IonToolbar,
  IonContent,
  IonTitle,
  IonButtons,
  IonMenuButton,
  IonList,
  IonListHeader,
  IonNote,
  IonMenuToggle,
  IonItem,
  IonIcon,
  IonLabel
} from "@ionic/vue";
import { useMainStore } from './store';
import { 
  homeOutline,
  settingsSharp,
  logOutSharp
} from 'ionicons/icons';

export default defineComponent({
  name: 'App',
  components: {
    IonApp,
    IonRouterOutlet,
    IonMenu,
    IonHeader,
    IonToolbar,
    IonContent,
    IonTitle,
    IonButtons,
    IonMenuButton,
    IonList,
    IonListHeader,
    IonNote,
    IonMenuToggle,
    IonItem,
    IonIcon,
    IonLabel
  },
  setup() {
    const store = useMainStore();
    const selectedIndex = ref(0);
    
    const appPages = [
      {
        title: 'Settings',
        url: '/settings',
        icon: settingsSharp
      },
      {
        title: 'Logout',
        url: '/logout',
        icon: logOutSharp
      },
    ];

    return {
      store,
      selectedIndex,
      appPages,
      homeOutline,
      settingsSharp,
      logOutSharp
    };
  }
});
</script>

<style>
ion-menu ion-content {
  --background: var(--ion-item-background, var(--ion-background-color, #ffffff));
}

ion-menu.md ion-content {
  --padding-start: 0;
  --padding-end: 0;
  --padding-top: 20px;
  --padding-bottom: 20px;
}

ion-menu.md ion-note {
  margin-bottom: 30px;
}

ion-menu.md ion-list-header,
ion-menu.md ion-note {
  padding-left: 33px;
}

ion-menu.md ion-list#inbox-list {
  border: 0;
}

ion-menu.md ion-list#inbox-list ion-list-header {
  font-size: 22px;
  font-weight: 700;
  min-height: 20px;
}

ion-menu.md ion-list#inbox-list ion-note {
  font-size: 16px;
  margin-bottom: 30px;
}

ion-menu.md ion-item {
  --padding-start: 33px;
  --inner-padding-end: 25px;
  font-weight: 500;
}

ion-menu.md ion-item.selected {
  --background: rgba(var(--ion-color-primary-rgb), 0.14);
}

ion-menu.md ion-item.selected ion-icon {
  color: var(--ion-color-primary);
}

ion-menu.md ion-item ion-icon {
  color: #616e7e;
}

ion-menu.md ion-item ion-icon.selected {
  color: var(--ion-color-primary);
}

ion-menu.ios ion-content {
  --padding-bottom: 20px;
}

ion-menu.ios ion-list {
  padding: 20px 0 0 0;
}

ion-menu.ios ion-note {
  line-height: 24px;
  margin-bottom: 20px;
}

ion-menu.ios ion-item {
  --padding-start: 16px;
  --inner-padding-end: 16px;
  font-weight: 400;
}

ion-menu.ios ion-item.selected ion-icon {
  color: var(--ion-color-primary);
}

ion-menu.ios ion-item ion-icon {
  font-size: 24px;
  color: #737373;
}

ion-item.selected {
  --color: var(--ion-color-primary);
}
</style>
