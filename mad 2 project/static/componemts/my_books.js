export default {
  template: `
    <div class="container mt-4">
      <div class="row">
        <div class="col-md-4">
          <div v-if="error" class="alert alert-danger">{{ error }}</div>
          <div class="card mb-4 shadow-sm" v-for="book in books_info" :key="book.book_id">
            <div class="card-body bg-secondary">
              <h5 class="card-title">Book Title: {{ book.book_name }}</h5>
              <p class="card-text">Book Author: {{ book.book_author }}</p>
              <button @click='read_book(book)' class="btn btn-primary">Read</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  `,
  data() {
    return {
      books_info: [],
      token: localStorage.getItem('auth-token'),
      email: localStorage.getItem('email'),
      error: null,
    };
  },
  methods: {
    read_book(book) {
      this.$router.push({ name: 'read_book', params: { book_id: book.book_id, book_name: book.book_name, book_author: book.book_author, book_content: book.book_content } });
    }
  },
  async mounted() {
    try {
      const res = await fetch('/my_books', {
        method: 'POST',
        headers: {
          'Authentication-Token': this.token,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email: this.email })
      });

      if (!res.ok) {
        this.error = `Error: ${res.statusText}`;
        return;
      }

      const data = await res.json();
      this.books_info = data;
    } catch (e) {
      this.error = 'An error occurred while fetching the data';
    }
  },
};
