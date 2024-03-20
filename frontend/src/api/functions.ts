import axios from 'axios'

import type { Location, PendingFriendRequests, PickleUser, RestrictedUser } from './types'

// USER FUNCTIONS //

/**
 * This function gets the information of the currently authenticated user.
 * @param baseUrl The base URL for the HTTP request.
 * @param logError Whether or not the error should be printed, if one occurs.
 * @returns a PickleUser object if the request is successful; undefined otherwise
 */
export async function getCurrentUser(baseUrl: string, logError: boolean): Promise<PickleUser | undefined> {
    try {
        const response = await axios.get(`${baseUrl}/current-user/`)
        if (response.data.user)
            return response.data.user
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
            return response.data.users
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