export default {
    template: `
      <div class="container mt-5">
        <div class="col-md-4">
          <label for="name">Title:</label>
          <input type="text" v-model="book.name" name="name" class="form-control" required>
        </div>
        <br>
        <div class="col-md-8">
          <label for="description">Author::</label>
          <input type="text" v-model="book.authors" name="description" class="form-control">
        </div>
        <div class="col-md-8">
          <label for="content">Content (URL):</label>
          <input type="url" v-model="book.content" class="form-control" id="content" name="content" required>
        </div>
        <br>
        <br>
        <button @click="updateBook" class="btn btn-primary">Update Book</button>
      </div>
    `,
    data() {
      return {
        book: {
          name: this.$route.params.book_name ,
          authors: this.$route.params.book_authors,
          content: this.$route.params.book_content
        },
        token: localStorage.getItem('auth-token')  // Assuming the token is stored in localStorage
      };
    },
    methods: {
      async updateBook() {
        const book_id = this.$route.params.book_id;  // Assuming you retrieve section_id from route params
        try {
          const res = await fetch(`/update_book/${book_id}`, {
            method: 'POST',
            headers: {
              'Authentication-Token': this.token,
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.book)
          });
  
          const data = await res.json().catch((e)=>{});
  
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
  