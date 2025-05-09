

export default {
    template: `
    <div>
            <div class="container mt-5">
                <div class="row justify-content-center">
                    <div class="col-md-6">
                        <div class="card">
                            <div class="card-header bg-success text-center text-white">
                                <h2> Registration</h2>
                            </div>
                                <div class="card-body">
                                    <div class="text-danger mb-3">{{ error }}</div>
                                    <div>
                                        <label for="username">Username:</label>
                                        <input type="text" v-model="user.username"  name="username" class="form-control" required>
                                    </div>
                                    <div>
                                        <label for="name">Name:</label>
                                        <input type="text" v-model="user.name"  name="name" class="form-control" required>
                                    </div>

                                    <div>
                                        <label for="email">Email:</label>
                                        <input type="email" v-model="user.email" id="email" name="email" class="form-control" required>
                                    </div>
                                    <div>
                                        <label for="password">Password:</label>
                                        <input type="password" v-model="user.password" id="password" name="password" class="form-control" required>
                                    </div>
                                    <br>
                                    <button type="submit" @click="register" class="btn btn-primary col-12 ">Register</button>
                                    <br>
                                    <br>
                                    <p class="mt-3 text-center">Already have an account? <router-link to="/login" >Login here</router-link> </p>
                                
                                </div>
                        </div>
                    </div>
                </div>
            </div>
    </div>
    `,
    data(){
        return {
            user:{username:null,
                name:null,
                email:null,
                password:null
        },
    error:null,}
    },
    
    methods: {
        async register() {
            try {
              const res = await fetch('/signup', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                },
                body: JSON.stringify(this.user),
              });
              const data = await res.json();
              if (res.ok) {
                this.$router.push({ path: '/login' });
              } else {
                this.error = data.message || "Registration failed.";
              }
            } catch (err) {
              console.error("Registration error:", err);
              this.error = "Server error. Please try again.";
            }
          }
          
      },
    }
