export type Post = {
  id: string
  user_id: string
  title: string
  text: string
  created_at: string
  updated_at: string
}

export type PostsPage = {
  items: Post[]
  has_more: boolean
}

