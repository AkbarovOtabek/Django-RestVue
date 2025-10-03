<template>
    <div class="page-sing-up">
        <div class="columns">
            <div class="column is-4 is-offset-4">
                <h1 class="title">Sing Up</h1>
                <form @submit.prevent="submitForm">
                    <div class="field">
                        <label>Username</label>
                        <div class="control">
                            <input type="text" class="input" v-model="username" required/>
                        </div>
                    </div>
                    <div class="field">
                        <label>Password</label>
                        <div class="control">
                            <input type="text" class="input" v-model="password" required/>
                        </div>
                    </div>
                    <div class="field">
                        <label>Repeat password</label>
                        <div class="control">
                            <input type="text" class="input" v-model="password2" required/>
                        </div>
                    </div>
                    <div class="notification is-danger" v-if="errors.length">
                        <p v-for="error in errors" :key="error">{{ error }}</p>
                    </div>
                     <div class="field">
                        <div class="control">
                            <button class="button is-dark">Sing Up</button>
                        </div>
                        <hr>
                        Or <router-link to="/log-in/">click here</router-link> to log in!
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>
<script>
import axios from "axios";
import {toast} from "bulma-toast";
export default {
  name: "SingUp",
  data() {
    return {
        username:'',
        password:'',
        password2:'',   
        errors:[]
    };
  },
  methods: {
    submitForm(){
        this.errors=[]
        if(this.username===''){
            this.errors.push('Username is missing')
        }
        if(this.password===''){
            this.errors.push('The password is to short')
        }
        if(this.password!==this.password2 ){
            this.errors.push('The passwords do not match')
        }
        if(!this.errors.length){
            const formData={
                username:this.username,
                password:this.password
            }
            axios.post("/api/v1/users/", formData).then(response=>{
                toast({
                    message: 'You have successfully registered! You can log in now.',
                    type: 'is-success',
                    duration: 2000,
                    dismissible: true,
                    pauseOnHover: true,
                  })
                this.$router.push('/log-in/')
            }).catch(error=>{
                if(error.response){
                    for(const key in error.response.data){
                        this.errors.push(`${key}: ${error.response.data[key]}`)
                    }
                }else if(error.request){
                    this.errors.push('An error occurred. Please try again.')
                    console.log(JSON.stringify(error))
                }
            })
        }
    }
  },
};
</script>