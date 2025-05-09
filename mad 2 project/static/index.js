import router from './router.js'
import Navbar from './componemts/navbar.js'
import login from './componemts/login.js'
import register from './componemts/register.js'
import home from './componemts/home.js'


new Vue({
    el: '#app',
    template: `<div>
    <Navbar :key='has_changed'/>
   
    <div v-show="show" class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card">
                <div class="card-body text-center">
                    <h2 class="mb-4">Welcome to Book Haven</h2>
                    
                    <br>
                    <img sec="" src="./static/assets/andy-vult-xdFzD2_iP9A-unsplash.jpg" alt="logo" width="500px" height="300px">
                    <br>
                    <br>

                    <button @click="login" class="btn btn-primary mb-3 col-8">Login</button>
                    <br>
                    <button @click="register" class="btn btn-success mb-3 col-8">Register</button>
                </div>
            </div>
        </div>
    </div>
</div>
       <router-view />
       </div>
    `,


    data(){
        return {
            show:true,
            has_changed:true,
        }
    },
    router,
    components:{
        Navbar,
        login,
        register,
        home,
    },
    watch:{
        $route(){
            this.has_changed=!this.has_changed
        }
    },

    methods:{
        login(){
            this.show=false;
            router.push({path:'/login'})

        },
        register(){
            this.show=false;
            router.push({path:'/register'})
        }

    
}})