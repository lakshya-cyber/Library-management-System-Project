import user_dashboard from './user_dashboard.js'    
import librarian_dashboard from './librarian_dashboard.js'


export default{
    template:`
    <div class="container">
        <user_dashboard v-if="userRole=='student'"/>
        <librarian_dashboard v-if="userRole=='admin'" />

    </div>
    `,
    data() {
        return {
          userRole: localStorage.getItem('role'),
          authToken: localStorage.getItem('auth-token'),
          
        }
      },
      components: {
        user_dashboard,
        librarian_dashboard
      }
}