import login from './componemts/login.js'
import home from './componemts/home.js'
import user_profile from './componemts/user_profile.js'
import librarian_dashboard from './componemts/librarian_dashboard.js'
import add_section from './componemts/add_section.js'
import register from './componemts/register.js'
import user_dashboard from './componemts/user_dashboard.js'
import sections from './componemts/sections.js'
import add_book from './componemts/add_book.js'
import librarian_requested from './componemts/librarian_requested.js'
import monitor_books from './componemts/monitor_books.js'
import librarian_stats from './componemts/librarian_stats.js'
import user_books from './componemts/user_books.js'
import my_books from './componemts/my_books.js'
import requested_books from './componemts/requested_books.js'
import book_summary from './componemts/book_summary.js'
import request_book from './componemts/request_book.js'
import update_section from './componemts/update_section.js'
import update_book from './componemts/update_book.js'
import read_book from './componemts/read_book.js'



const routes = [
  { path: '/login', component: login, name: 'login' },
  {path:'/librarian_dashboard',component:librarian_dashboard,name:'librarian_dashboard'},
  {path:'/register',component:register,name:'register'},
  {path:'/home',component:home,name:'home'},
  {path:'/add_section',component:add_section,name:'add_section'},
  {path:'/sections',component:sections,name:'sections'},
  {path:'/update_section/:section_id',component:update_section,name:'update_section'}, 
  {path:'/book/:section_id',component:add_book,name:'add_book'},
  {path:'/update_book/:book_id',component:update_book,name:'update_book'},
  {path:'/book_summary/:section_id',component:book_summary,name:'book_summary'},
  {path:'/librarian_requested',component:librarian_requested,name:'librarian_requested'},
  {path:'/monitor_books',component:monitor_books,name:'monitor_books'},
  {path:'/librarian_stats',component:librarian_stats,name:'librarian_stats'},


  
  {path:'/user_dashboard',component:user_dashboard,name:'user_dashboard'},
  {path:'/user_profile',component:user_profile,name:'user_profile'},
  {path:'/user_books',component:user_books,name:'user_books'},
  {path:'/request_book/:book_id',component:request_book,name:'request_book'},
  {path:'/my_books',component:my_books,name:'my_books'},
  {path:'/read_book/:book_id',component:read_book,name:'read_book'},
  {path:'/requested_books',component:requested_books,name:'requested_books'}

  
]

export default new VueRouter({
  routes,
})
