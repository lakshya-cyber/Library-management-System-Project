export default {
  template: `
    <div class="container mt-5">
      <div class="col-md-4">
        <div v-if="error" class="alert alert-danger">{{ error }}</div>
        <label for="name">Title:</label>
        <input type="text" v-model="section.name" name="name" class="form-control" required>
      </div>
      <br>
      <div class="col-md-8">
        <label for="description">Description:</label>
        <input type="text" v-model="section.description" name="description" class="form-control">
      </div>
      <br>
      <br>
      <button @click="addSection" class="btn btn-primary">Add Section</button>
      
    </div>
  `,
  data() {
    return {
      section: {
        name: null,
        description: null
      },
      error: null,
      token: localStorage.getItem('auth-token')  // Assuming the token is stored in localStorage
    }
  },
  methods: {
   async addSection() {
      const res = await fetch('/add_section', {
        method: 'POST',
        headers: {
          
          'Authentication-Token': this.token,
          
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(this.section)
      })
      
      const data = await res.json().catch((e)=>{})
     
      if (res.ok) {
       
        this.$router.push({ path: '/sections' })
      } 
    }
  }
}