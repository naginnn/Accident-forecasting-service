export const getAuthHeader = () => {
    return {Authorization: 'Bearer ' + localStorage.getItem('token')}
}