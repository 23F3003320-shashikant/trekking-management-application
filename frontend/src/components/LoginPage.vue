<template>
    <div>
        <h1>Login</h1>
        <div>
        <form @submit.prevent="Loggon">
            <label for="email_id">Email</label>
            <input type="email" v-model="form.email_id" placeholder="Enter your email">
            <label for="password">Password</label>
            <input type="password" v-model="form.password" placeholder="Enter your password">
            <button type="submit">Login</button>
        </form>
        </div>
    </div>
</template>
<script>
import axios from 'axios';

 export default {
    name: 'LoginPage',
    data() {
        return {
            form: {
            email_id: '',
            password: ''
            }
        }
    },
    methods: {
    async Loggon(){
        try{
            const response = await axios.post('http://localhost:5000/login', {
                email_id:this.form.email_id,
                password:this.form.password,
            });

            console.log("login successfully:", response.data);
            localStorage.setItem('token', response.data.access_token)
            const role =response.data.role
            console.log("ROLE =", role);

            if (role === 'admin') {
                this.$router.push('/admin');
            }

            if  (role === 'staff'){
                this.$router.push('/staff');
            }
            if (role=='trekker'){
                this.$router.push('/trekker');
            }
        }
        catch(error){
            console.error("login error:", error);
        }

    }
 }
}
 
</script>