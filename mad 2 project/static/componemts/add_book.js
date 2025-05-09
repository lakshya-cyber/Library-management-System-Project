export default {
  template: `
    <div class="container mt-5 card-body">
      <div class="container">
        <h2>Add New Book</h2>
        <br>
        <div class="col-md-4">
          <label for="title">Title:</label>
          <input type="text" v-model="book.name" class="form-control" id="title" name="title" required>
        </div>
        <br>
        <div class="col-md-4">
          <label for="author">Author:</label>
          <input type="text" v-model="book.authors" class="form-control" id="author" name="author" required>
        </div>
        <br>
        <div class="col-md-8">
          <label for="content">Content (URL):</label>
          <input type="url" v-model="book.content" class="form-control" id="content" name="content" required>
        </div>
        <br>
        <br>
        <button @click="addBook" type="submit" class="btn btn-primary">Add Book</button>
      </div>
    </div>
  `,
  data() {
    return {
      book: {
        name: null,
        authors: null,
        content: null,
      },
      token: localStorage.getItem('auth-token'),
      section_name: this.$route.params.section_name,
      section_id: this.$route.params.section_id,
      error: null,
    };
  },
  methods: {
    async addBook() {
      try {
        const res = await fetch(`/book/${this.section_id}`, {
          method: 'POST',
          headers: {
            'Authentication-Token': this.token,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.book),
        });

        if (!res.ok) {
          const errorData = await res.json();
          this.error = errorData.message || 'An error occurred';
          return;
        }

        this.$router.push({ path: '/sections' });
      } catch (e) {
        this.error = 'An error occurred';
      }
    },
  },
};
