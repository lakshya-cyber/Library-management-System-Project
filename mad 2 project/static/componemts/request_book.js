export default {
    template: `
      <div class="container">
        <h1>Request Book</h1>
        <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
        <div class="form-group">
          <label for="day_request">Requested Days:</label>
          <input type="number" v-model="book.day_request" class="form-control" id="day_request" name="day_request" required>
        </div>
        <button type="submit" @click="requestBook" class="btn btn-primary">Request</button>
        
      </div>
    `,
    data() {
      return {
        book: {
          name: this.$route.params.name,
          day_request: null,
          user: localStorage.getItem('email'),
        },
        token: localStorage.getItem('auth-token'),
        error: null,
        book_id: this.$route.params.book_id
      };
    },
    methods: {
      async requestBook() {
        try {
          const res = await fetch(`/request_book/${this.book_id}`, {
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
  
          this.$router.push({ path: '/user_dashboard' });
        } catch (e) {
          this.error = 'An error occurred';
        }
      }
    }
  };
  