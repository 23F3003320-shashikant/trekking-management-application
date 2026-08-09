<template>
    <div>
        home page
        <div>
            <LoginPage/>
        </div>
    </div>
</template>

<script>
import LoginPage from '../components/LoginPage.vue';
export default{
    name : "HomeView",
    components:{
        LoginPage
    }
}
</script>