export default {
    template: `
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark ">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">Book Haven</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item" v-if="role=='admin'">
            <router-link class="nav-link" to="/sections">Section Details</router-link>
          </li>
          <li class="nav-item" v-if="role=='admin'">
            <router-link class="nav-link" to="/add_section">Add Section</router-link>
          </li>
          <li class="nav-item" v-if="role=='admin'">
            <router-link class="nav-link" to="/librarian_requested">Librarian Request</router-link>
          </li>
          <li class="nav-item" v-if="role=='admin'">
            <router-link class="nav-link" to="/monitor_books">Monitor Books</router-link>
          <li class="nav-item" v-if="role=='admin'">
            <router-link class="nav-link" to="/librarian_stats">Statistics</router-link>
          </li>            
          </li>
           <li class="nav-item" v-if="role=='student'">
            <router-link class="nav-link" to="/user_dashboard">Dashboard</router-link>
          </li>
          <li class="nav-item" v-if="role=='student'">
            <router-link class="nav-link" to="/user_books">Books</router-link>
          </li>
          <li class="nav-item" v-if="role=='student'">
            <router-link class="nav-link" to="/my_books">My Books</router-link>
          </li>
          <li class="nav-item" v-if="role=='student'">
            <router-link class="nav-link" to="/requested_books">Requested Books</router-link>
          </li>
          <li class="nav-item" v-if="is_login">
            <button class="nav-link" @click='logout' >logout</button>
          </li>
        </ul>
      </div>
    </div>
  </nav>`,
    data() {
      return {
        role: localStorage.getItem('role'),
        is_login: localStorage.getItem('auth-token'),
        email: localStorage.getItem('email'),
      }
    },
    methods: {
      logout() {
        localStorage.removeItem('auth-token')
        localStorage.removeItem('role')
        localStorage.removeItem('email')
        this.$router.push({ path: '/login' })
      },
    },
  }
  