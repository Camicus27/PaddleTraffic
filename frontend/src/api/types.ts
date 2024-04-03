export interface PickleUser {
  id: number
  username: string
  first_name: string | null
  last_name: string | null
  email: string | null
  groups: Array<string> // Not sure if groups are strings yet, they're probably their own object type
  is_staff: boolean
  is_active: boolean
  is_superuser: boolean
  last_login: string
  date_joined: string
  friends: Array<RestrictedUser>
  matches_attended: number
  matches_created: number
  win_count: number
  loss_count: number
  skill_level:
  | 'Beginner'
  | 'Advanced Beginner'
  | 'Intermediate Beginner'
  | 'Intermediate'
  | 'Advanced Intermediate'
  | 'Expert'
  | 'Advanced Expert'
  | 'Professional'
  bio: string
  is_member: boolean
  latitude: number | null
  longitude: number | null
}

export interface RestrictedUser {
  id: number
  username: string
  first_name: string | null
  last_name: string | null
  matches_attended: number
  matches_created: number
  win_count: number
  loss_count: number
  skill_level:
  | 'Beginner'
  | 'Advanced Beginner'
  | 'Intermediate Beginner'
  | 'Intermediate'
  | 'Advanced Intermediate'
  | 'Expert'
  | 'Advanced Expert'
  | 'Professional'
  bio: string
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
  calculated_time: string
}

export interface Report {
    courts_occupied: number,
    number_waiting: number
}

export interface Event {
  id: number
  name: string
  description: string
  location: Location
  host: RestrictedUser
  players: Array<RestrictedUser>
  date: string
  time: string
  isPublic: boolean
}

export interface FriendRequest {
  id: number
  requester: RestrictedUser
  receiver: RestrictedUser
  date_created: string
  accepted: boolean
}

export interface PendingFriendRequests {
  incoming_requests: Array<FriendRequest>
  outgoing_requests: Array<FriendRequest>
}