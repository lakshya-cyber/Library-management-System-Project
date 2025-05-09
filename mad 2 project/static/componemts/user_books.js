export default {
  template: `
    <div class="container mt-5">
      <div class="alert alert-danger" v-if="error">{{ error }}</div>
      <div class="mb-3 col-md-6 justify-content-center">
        <input
          v-model="searchQuery"
          type="text"
          class="form-control"
          placeholder="Search books..."
          @input="filterBooks"
        />
      </div>
      <table class="table table-bordered table-hover table-dark">
        <thead>
          <tr>
            <th>Name</th>
            <th>Author</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="book in filteredBooks" :key="book.book_id">
            <td>{{ book.name }}</td>
            <td>{{ book.authors }}</td>
            <td>
              <button @click="requestBook(book.book_id)" class="btn btn-primary btn-sm">Request</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  `,
  data() {
    return {
      books: [],
      token: localStorage.getItem('auth-token'),
      error: null,
      searchQuery: '',
      filteredBooks: [],
    };
  },
  methods: {
    async requestBook(book_id) {
      this.$router.push({ name: 'request_book', params: { book_id } });
    },
    filterBooks() {
      const query = this.searchQuery.toLowerCase();
      this.filteredBooks = this.books.filter(book =>
        book.name.toLowerCase().includes(query) || book.authors.toLowerCase().includes(query)
      );
    },
  },
  async mounted() {
    try {
      const res = await fetch('/user_books', {
        headers: {
          'Authentication-Token': this.token,
        },
      });

      if (!res.ok) {
        this.error = `Error: ${res.statusText}`;
        return;
      }

      const data = await res.json();
      this.books = data;
      this.filteredBooks = data; // Initialize filteredBooks with all books
    } catch (e) {
      this.error = 'An error occurred while fetching the data';
    }
  },
};
