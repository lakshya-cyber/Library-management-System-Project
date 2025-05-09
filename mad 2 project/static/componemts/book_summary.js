export default {
  template: `
    <div class="container mt-5">
      <div v-if="error" class="alert alert-danger">{{ error }}</div>
      <div class="d-flex justify-content-between mb-4">
        <input v-model="searchQuery" @input="filterBooks" placeholder="Search books" class="form-control me-2" />
      </div>
      <table class="table table-bordered table-hover table-success">
        <thead>
          <tr>
            <th>Name</th>
            <th>Author</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="book in filteredBooks" :key="book.book_id">
            <td>{{ book.name }}</td>
            <td>{{ book.authors }}</td>
            <td>
              <button @click="updateBook(book)" class="btn btn-primary btn-sm me-2">Update</button>
              <button @click="deleteBook(book.book_id)" class="btn btn-danger btn-sm">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  `,
  data() {
    return {
      books: [],
      filteredBooks: [],
      searchQuery: '',
      token: localStorage.getItem('auth-token'),
      section_id: this.$route.params.section_id,
      error: null,
    };
  },
  methods: {
    updateBook(book) {
      this.$router.push({
        name: 'update_book',
        params: {
          book_id: book.book_id,
          book_name: book.name,
          book_authors: book.authors,
          book_content: book.content,
        },
      });
    },

    async deleteBook(book_id) {
      try {
        const res = await fetch(`/delete_book/${book_id}`, {
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
        this.books = this.books.filter(book => book.book_id !== book_id);
        this.filteredBooks = this.filteredBooks.filter(book => book.book_id !== book_id);
      } catch (e) {
        this.error = 'An error occurred while deleting the book';
      }
    },
    
    filterBooks() {
      this.filteredBooks = this.books.filter(book =>
        book.name.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    }
  },
  async mounted() {
    try {
      const res = await fetch(`/book_summary/${this.section_id}`, {
        headers: {
          'Authentication-Token': this.token,
        },
      });

      if (!res.ok) {
        this.error = `Error: ${res.statusText}`;
        console.error('Failed to fetch books:', await res.text());
        return;
      }

      const data = await res.json();
      this.books = data;
      this.filteredBooks = data; // Initialize filteredBooks with all books
    } catch (e) {
      this.error = 'An error occurred while fetching the data';
      console.error('Fetch error:', e);
    }
  },
};
