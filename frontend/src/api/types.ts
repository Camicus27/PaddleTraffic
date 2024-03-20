export interface PickleUser {
  id: number
  username: String
  first_name: String | null
  last_name: String | null
  email: String | null
  groups: Array<String> // Not sure if groups are strings yet, they're probably their own object
  is_staff: Boolean
  is_active: Boolean
  is_superuser: Boolean
  last_login: String
  date_joined: String
  friends: Array<RestrictedUser>
  matches_attended: Number
  matches_created: Number
  win_count: Number
  loss_count: Number
  skill_level:
  | 'Beginner'
  | 'Advanced Beginner'
  | 'Intermediate Beginner'
  | 'Intermediate'
  | 'Advanced Intermediate'
  | 'Expert'
  | 'Advanced Expert'
  | 'Professional'
  bio: String
  is_member: boolean
  latitude: Number | null
  longitude: Number | null
}

export interface RestrictedUser {
  id: Number
  username: String
  first_name: String | null
  last_name: String | null
  matches_attended: Number
  matches_created: Number
  win_count: Number
  loss_count: Number
  skill_level:
  | 'Beginner'
  | 'Advanced Beginner'
  | 'Intermediate Beginner'
  | 'Intermediate'
  | 'Advanced Intermediate'
  | 'Expert'
  | 'Advanced Expert'
  | 'Professional'
  bio: String
}

export interface Location {
  id: number
  name: string
  latitude: number
  longitude: number
  court_count: number
  courts_occupied: number
  number_waiting: number
  estimated_wait_time: number
}