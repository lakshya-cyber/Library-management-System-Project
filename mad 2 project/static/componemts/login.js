import Navbar from './navbar.js'
export default {
    template: `
    <div>
        <div class="container mt-5">
            <div class="row justify-content-center">
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header bg-secondary text-center text-white">
                            <h2> Login</h2>
                        </div>
                        <div class="card-body">
                            <div class="text-danger mb-3">{{ error }}</div>
                            <div>
                                <label for="email">Email:</label>
                                <input type="email" id="email" name="email" v-model="librarian.email" class="form-control" required>
                            </div>
                            <div>
                                <label for="password">Password:</label>
                                <input type="password" id="password" name="password" v-model="librarian.password" class="form-control" required>
                            </div>
                            <br>
                            <button @click="login" class="btn btn-primary col-12 btn btn-primary">Login</button>
                            <br>
                            <br>
                            <p class="mt-3 text-center">Don't have an account? <router-link to="/register" >Register here</router-link> </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    `,
    data() {
        return {
            librarian: {
                email: null,
                password: null,
            },
            error: null
            
        };
    },
    components: {
        Navbar
    },
    methods: {
        async login() {
          const res = await fetch('/librarian_login', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(this.librarian),
          })
          const data = await res.json()
          if (res.ok) {
            localStorage.setItem('auth-token', data.token)
            localStorage.setItem('role', data.role)
            localStorage.setItem('email', data.email)
            this.$router.push({ path: '/home' })
          } else {
            this.error = data.message
          }
        },
      },
    }