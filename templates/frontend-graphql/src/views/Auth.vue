<template>
  <ion-page>
    <ion-content>
      <ion-grid class="full-height">    
        <ion-row class="ion-align-items-center ion-justify-content-center full-height">
          <ion-col></ion-col>

          <ion-col size="12" size-md="6" size-lg="4">
            <ion-card>

              <ion-card-header>
                <ion-card-title color="primary">   
                  <h1>
                    {{ isLogin ? 'Welcome back' : 'Sign up' }}
                  </h1>
                </ion-card-title>
                <ion-card-subtitle>
                  {{ isLogin ? 'Sign in to your account' : '' }}
                </ion-card-subtitle>
              </ion-card-header>

              <ion-card-content>       
                <ion-row v-if="!isLogin">
                  <ion-col style="padding-left:0;">
                    <ion-input shape="round" fill="outline" label-placement="floating" label="First Name" v-model="firstName" required></ion-input>
                  </ion-col>
                  <ion-col style="padding-right:0;">
                    <ion-input shape="round" fill="outline" label-placement="floating" label="Last Name" v-model="lastName" required></ion-input>
                  </ion-col>
                </ion-row>
                <br/>
                <ion-input shape="round" fill="outline" label-placement="floating" label="Email" v-model="email" type="email" required></ion-input>
                <br/> 
                <ion-input shape="round" fill="outline" label-placement="floating" label="Password" type="password" v-model="password" required :error-text="error"></ion-input>
                <br/> 

                <ion-button size="large" shape="round" expand="full" :disabled="isSubmitting" @click="handleSubmit">
                  Continue
                </ion-button>
                <br/> 
                <!-- <ion-text color="danger" v-if="error" class="ion-text-center">{{ error }}</ion-text> -->

                <div class="align-items">
                  <ion-text>{{ isLogin ? "Don't have an account? " : 'Already a member? ' }}</ion-text>
                  <ion-button size="small" shape="round" @click="toggleAuth" fill="clear">
                    {{ isLogin ? 'Sign up' : 'Login' }}
                  </ion-button>
                </div>   
              </ion-card-content>
            </ion-card>
          </ion-col>

          <ion-col></ion-col>
        </ion-row> 
      </ion-grid>
    </ion-content>
  </ion-page>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useIonRouter } from '@ionic/vue';
import { useMainStore } from '../store';
import {
  IonContent,
  IonPage,
  IonInput,
  IonButton,
  IonText,
  IonGrid,
  IonRow,
  IonCol,
  IonCard,
  IonCardContent,
  IonCardHeader,
  IonCardTitle,
  IonCardSubtitle,
  IonItem,
  IonList,
} from '@ionic/vue';
import { LoginRequest, RegisterRequest, model as authModel } from '../services/auth/auth.model';

export default defineComponent({
  name: 'Auth',
  components: {
    IonContent,
    IonPage,
    IonInput,
    IonButton,
    IonText,
    IonGrid,
    IonRow,
    IonCol,
    IonCard,
    IonCardContent,
    IonCardHeader,
    IonCardTitle,
    IonCardSubtitle,
    IonItem,
    IonList,
  },
  setup() {
    const store = useMainStore();
    const router = useIonRouter();

    const password = ref('');
    const email = ref('');
    const firstName = ref('');
    const lastName = ref('');
    const isLogin = ref(true);
    const error = ref('');
    const isSubmitting = ref(false);

    const handleSubmit = async () => {
      error.value = '';
      isSubmitting.value = true;

      try {
        let response;
        if (isLogin.value) {
          const loginData: LoginRequest = { email: email.value, password: password.value };
          response = await authModel.api.login(loginData);
        } else {
          const registerData: RegisterRequest = {
            password: password.value,
            email: email.value,
            firstName: firstName.value,
            lastName: lastName.value,
          };
          response = await authModel.api.register(registerData);
        }

        store.setAuth(true);
        store.setUser(response.user);

        router.push('/home');
      } catch (e) {
        error.value = e instanceof Error ? e.message : 'An error occurred';
      } finally {
        isSubmitting.value = false;
      }
    };

    const toggleAuth = () => {
      isLogin.value = !isLogin.value;
      password.value = '';
      email.value = '';
      firstName.value = '';
      lastName.value = '';
      error.value = '';
    };

    return {
      password,
      email,
      firstName,
      lastName,
      isLogin,
      isSubmitting,
      handleSubmit,
      toggleAuth,
      error,
    };
  },
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