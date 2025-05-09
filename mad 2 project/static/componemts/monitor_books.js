export default {
  template: `
    <div class="container mt-5">
      <h1>Monitor Books</h1>
      <div v-if="error" class="alert alert-danger">{{ error }}</div>
      <table class="table table-hover table-dark">
        <thead>
          <tr>
            <th>Book Name</th>
            <th>Book Author</th>
            <th>Issued To</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="book_info in books_info" :key="book_info.book_id">
            <td>{{ book_info.book_name }}</td>
            <td>{{ book_info.book_author }}</td>
            <td>{{ book_info.user_email }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  `,
  data() {
    return {
      books_info: [],
      token: localStorage.getItem('auth-token'),
      error: null,
    };
  },
  async mounted() {
    try {
      const res = await fetch('/monitor_books', {
        headers: {
          'Authentication-Token': this.token,
        },
      });

      if (!res.ok) {
        this.error = `Error: ${res.statusText}`;
        return;
      }

      const data = await res.json().catch((e)=>{});
      this.books_info = data;
    } catch (e) {
      this.error = 'An error occurred while fetching the data';
    }
  },
};
