import axios from 'axios'

import type { FriendRequest, Location, PendingFriendRequests, PickleUser, RestrictedUser } from './types'

// USER FUNCTIONS //

/**
 * This function fetches the information of the currently authenticated user.
 * @param baseUrl The base URL for the HTTP request.
 * @param logError Whether or not the error should be printed, if one occurs.
 * @returns a PickleUser object if the request is successful; undefined otherwise
 */
export async function getCurrentUser(baseUrl: string, logError: boolean): Promise<PickleUser | undefined> {
    try {
        const response = await axios.get(`${baseUrl}/current-user/`)
        if (response.data.user)
            return response.data.user as PickleUser
    } catch (error) {
        if (logError)
            console.error(error)
    }
    return undefined
}

/**
 * This function fetches all users from the server.
 * @param baseUrl The base URL for the HTTP request.
 * @param logError Whether or not the error should be printed, if one occurs.
 * @returns An array of RestrictedUser objects if the request is successful; undefined otherwise.
 */
export async function getAllUsers(baseUrl: string, logError: boolean): Promise<Array<RestrictedUser> | undefined> {
    try {
        const response = await axios.get(`${baseUrl}/users/`)
        if (response.data.users)
            return response.data.users as Array<RestrictedUser>
    } catch (error) {
        if (logError)
            console.error(error)
    }
    return undefined
}

/**
 * This function fetches a user with a given ID from the server.
 * @param id The ID of the requested user.
 * @param baseUrl The base URL for the HTTP request.
 * @param logError Whether or not the error should be printed, if one occurs.
 * @returns A RestrictedUser object if the request is successful; undefined otherwise.
 */
export async function getUserId(id: number, baseUrl: string, logError: boolean): Promise<RestrictedUser | undefined> {
    try {
        const response = await axios.get(`${baseUrl}/users/${id}/`)
        if (response.data.user)
            return response.data.user as RestrictedUser
    } catch (error) {
        if (logError)
            console.error(error)
    }
    return undefined
}

/**
 * This function fetches a user with a given username from the server.
 * @param id The username of the requested user.
 * @param baseUrl The base URL for the HTTP request.
 * @param logError Whether or not the error should be printed, if one occurs.
 * @returns A RestrictedUser object if the request is successful; undefined otherwise.
 */
export async function getUserUsername(username: string, baseUrl: string, logError: boolean): Promise<RestrictedUser | undefined> {
    try {
        const response = await axios.get(`${baseUrl}/users/${username}/`)
        if (response.data.user)
            return response.data.user as RestrictedUser
    } catch (error) {
        if (logError)
            console.error(error)
    }
    return undefined
}


// LOCATION FUNCTIONS //

/**
 * This function fetches all available locations from the server.
 * @param baseUrl The base URL for the HTTP request.
 * @param logError Whether or not the error should be printed, if one occurs.
 * @returns An array of Location objects if the request is successful; undefined otherwise.
 */
export async function getAllLocations(baseUrl: string, logError: boolean): Promise<Array<Location> | undefined> {
    try {
        const response = await axios.get(`${baseUrl}/locations/`)
        if (response.data.locations)
            return response.data.locations as Array<Location>
    } catch (error) {
        if (logError)
            console.error(error)
    }
    return undefined
}


/**
 * This function fetches a location with a given ID from the server.
 * @param id The ID of the requested location.
 * @param baseUrl The base URL for the HTTP request.
 * @param logError Whether or not the error should be printed, if one occurs.
 * @returns A Location object if the request is successful; undefined otherwise.
 */
export async function getLocationId(id: number, baseUrl: string, logError: boolean): Promise<Location | undefined> {
    try {
        const response = await axios.get(`${baseUrl}/locations/${id}/`)
        if (response.data.location)
            return response.data.location as Location
    } catch (error) {
        if (logError)
            console.error(error)
    }
    return undefined
}

// EVENT FUNCTIONS //

// TODO: Fill in event functions


// FRIEND REQUEST FUNCTIONS //

/**
 * This function retrieves pending friend requests for the authenticated user.
 * @param baseUrl The base URL for the HTTP request.
 * @param logError Whether or not the error should be printed, if one occurs.
 * @returns A PendingFriendRequests object if the request is successful; undefined otherwise.
 */
export async function getFriendRequests(baseUrl: string, logError: boolean): Promise<PendingFriendRequests | undefined> {
    try {
        const response = await axios.get(`${baseUrl}/friend-requests/`, { withCredentials: true })
        return response.data as PendingFriendRequests
    } catch (error) {
        if (logError)
            console.error(error)
    }
    return undefined
}


/**
 * This function fetches a friend request with the given ID from the server.
 * @param id The ID of the requested friend request.
 * @param baseUrl The base URL for the HTTP request.
 * @param logError Whether or not the error should be printed, if one occurs.
 * @returns A FriendRequest object if the request is successful; undefined otherwise.
 */
export async function getFriendRequestId(id: number, baseUrl: string, logError: boolean): Promise<FriendRequest | undefined> {
    try {
        const response = await axios.get(`${baseUrl}/friend-requests/${id}/`)
        if (response.data.friend_request)
            return response.data.friend_request as FriendRequest
    } catch (error) {
        if (logError)
            console.error(error)
    }
    return undefined
}


/**
 * This function creates a friend request from the currently authenticated user to the user with userId.
 * @param userId The ID of the user that will receive the friend request.
 * @param baseUrl The base URL for the HTTP request.
 * @param logError Whether or not the error should be printed, if one occurs.
 * @returns True if the request is successful; false otherwise.
 */
export async function createFriendRequest(userId: number, baseUrl: string, logError: boolean): Promise<boolean> {
    try {
        await axios.post(`${baseUrl}/friend-requests/${userId}/`)
        return true
    } catch (error) {
        if (logError)
            console.error(error)
        return false
    }
}


/**
 * This function deletes a friend request with the given ID from the server.
 * @param id The ID of the friend request.
 * @param baseUrl The base URL for the HTTP request.
 * @param logError Whether or not the error should be printed, if one occurs.
 * @returns True if the request is successful; false otherwise.
 */
export async function deleteFriendRequest(id: number, baseUrl: string, logError: boolean): Promise<boolean> {
    try {
        await axios.delete(`${baseUrl}/friend-requests/${id}/`)
        return true
    } catch (error) {
        if (logError)
            console.error(error)
        return false
    }
}


/**
 * This function sends a request to accept the friend request with the given ID to the server.
 * @param id The ID of the friend request.
 * @param baseUrl The base URL for the HTTP request.
 * @param logError Whether or not the error should be printed, if one occurs.
 * @returns True if the request is successful; false otherwise.
 */
export async function acceptFriendRequest(id: number, baseUrl: string, logError: boolean): Promise<boolean> {
    try {
        await axios.post(`${baseUrl}/friend-requests/accept/${id}/`)
        return true
    } catch (error) {
        if (logError)
            console.error(error)
        return false
    }
}