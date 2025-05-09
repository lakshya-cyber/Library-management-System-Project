export default {
  template: `
    <div class="container mt-5">
      <div v-if="error" class="alert alert-danger">{{ error }}</div>
      <div v-if="book">
        <h3>Book Name: {{ book.name }}</h3>
        <h3>Authors: {{ book.author }}</h3>
        <h3>Book Content: {{ book.content }}</h3>
        <input type="text" v-model="feedback" name="feedback" class="form-control">
        <button @click="addFeedback" class="btn btn-primary">Submit Feedback</button>
      </div>
    </div>
  `,
  data() {
    return {
      book: null,
      token: localStorage.getItem('auth-token'),
      error: null,
      feedback: null,
      book_id: this.$route.params.book_id
    };
  },
  methods: {
    async addFeedback() {
      try {
        const res = await fetch(`/add_feedback/${this.book_id}`, {
          method: 'POST',
          headers: {
            'Authentication-Token': this.token,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ feedback: this.feedback })
        });
        
        const data = await res.json();
        
        if (res.ok) {
          this.$router.push({ path: '/my_books' });
        } else {
          this.error = data.message || 'An error occurred';
        }
      } catch (e) {
        this.error = 'An error occurred while submitting the feedback';
      }
    }
  },

  async mounted() {
    try {
      const res = await fetch(`/read_book/${this.book_id}`, {
        headers: {
          'Authentication-Token': this.token
        }
      });
      if (!res.ok) {
        this.error = `Error: ${res.statusText}`;
        return;
      }
      const data = await res.json();
      this.book = data;
    } catch (e) {
      this.error = 'An error occurred while fetching the data';
    }
  }
};
