import axios from 'axios';

const axiosWithAuth = () => {
  const token = localStorage.getItem('token');

  return axios.create({
    headers: {
      Authorization: `Bearer ${token}`
    },
    baseURL: 'https://rocket-challenge-joelp.herokuapp.com/' //CHANGE BASE URL
  });
};

export default axiosWithAuth;
