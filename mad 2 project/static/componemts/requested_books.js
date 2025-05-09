export default {
  template: `
    <div class="container mt-5">
      <div class="alert alert-danger" v-if="error">{{ error }}</div>
      <div class="row">
        <div  class="col-md-6">
          <table class="table table-bordered">
            <thead>
              <tr>
                <th>Title</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="book in userBooks" :key="book.book_id">
                <td>{{ book.book_name }}</td>
                <td v-if="book.status == 0">
                  <button @click="deleteBook(book.book_id)" class="btn btn-danger">Delete book</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  `,
  data() {
    return {
      requested_books: [],
      token: localStorage.getItem('auth-token'),
      email: localStorage.getItem('email'),
      error: null,
    };
  },
  computed: {
    userBooks() {
      return this.requested_books.filter(book => book.user_email === this.email);
    }
  },
  methods: {
    async deleteBook(book_id) {
      try {
        const res = await fetch(`/request_delete_book/${book_id}`, {
          method: 'DELETE',
          headers: {
            'Authentication-Token': this.token,
          },
        });

        if (!res.ok) {
          const errorData = await res.json();
          this.error = errorData.message || 'An error occurred';
          return;
        }

        // Remove the deleted book from the list
        this.requested_books = this.requested_books.filter(book => book.book_id !== book_id);
      } catch (e) {
        this.error = 'An error occurred while deleting the book';
      }
    },
  },
  async mounted() {
    try {
      const res = await fetch('/requested_books', {
        headers: {
          'Authentication-Token': this.token,
        },
      });

      if (!res.ok) {
        this.error = `Error: ${res.statusText}`;
        return;
      }

      const data = await res.json();
      this.requested_books = data;
    } catch (e) {
      this.error = 'An error occurred while fetching the data';
    }
  },
};
