export default {
    template: `
      <div class="container mt-5">
        <div class="col-md-4">
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
        <button @click="updateSection" class="btn btn-primary">Update Section</button>
      </div>
    `,
    data() {
      return {
        section: {
          name: this.$route.params.section_name ,
          description: this.$route.params.section_description
        },
        token: localStorage.getItem('auth-token')  // Assuming the token is stored in localStorage
      };
    },
    methods: {
      async updateSection() {
        const section_id = this.$route.params.section_id;  // Assuming you retrieve section_id from route params
        try {
          const res = await fetch(`/update_section/${section_id}`, {
            method: 'POST',
            headers: {
              'Authentication-Token': this.token,
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.section)
          });
  
          const data = await res.json();
  
          if (res.ok) {
            // Successfully updated, navigate to sections page or any other appropriate route
            this.$router.push({ path: '/sections' });
          } else {
            // Handle errors
            console.error('Failed to update section:', data.message || 'Unknown error');
          }
        } catch (error) {
          console.error('An error occurred while updating section:', error.message);
        }
      }
    }
  };
  